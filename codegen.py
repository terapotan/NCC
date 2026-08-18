# -*- coding: utf-8 -*-
"""
NC16C コード生成器 (codegen)

生成方針の要点（詳細はGRAMMAR.mdを参照）：
- レジスタ数が少ない(a,b,c,d,e,bp,sp)ため、式評価は「スタックベース」で行う。
  部分式の結果は基本的にレジスタaに置き、必要な間はハードウェアスタックにpushして
  退避する。これによりレジスタ割り付けの複雑なアルゴリズムを避け、正しさを優先する。
- 関数呼び出しは、引数を右から左へpushするcdecl風の呼び出し規約を採用する。
  呼び出し後、bp+2が第1引数、bp+3が第2引数、…となる。
- 比較命令(jl/jle/ja/jae)はNC-16の仕様上「符号フラグのみ」で判定される、つまり
  符号付き比較である。uint型は0～65535の符号なし整数として扱いたいため、
  比較の直前に両オペランドの最上位ビットをxor 0x8000で反転させてから比較する
  （signed<->unsignedの順序を保つビット変換テクニック）。
"""
from ast_nodes import *
from symtab import (
    Type, PrimType, PointerType, ArrayType, StructType, Symbol, FuncSig, Scope,
    UINT, CHAR, BOOL, resolve_typename, CompileError,
)
from nc16_builtins import BUILTIN_SIGNATURES


def is_ptr_like(t):
    return isinstance(t, (PointerType, ArrayType))


class CodeGen:
    def __init__(self):
        self.structs = {}
        self.globals = {}
        self.funcs = {}
        self.func_asm = []
        self.data_asm = []
        self.string_pool = {}
        self.label_counter = 0
        self.loop_labels = []    # スタック: (continue_label, break_label)
        self.switch_break_labels = []
        self.cur_func_name = None
        self.cur_ret_type = None
        self.cur_epilogue = None

    # ---------------------------------------------------------------
    # ユーティリティ
    # ---------------------------------------------------------------
    def new_label(self, hint='L'):
        self.label_counter += 1
        return f"_{hint}_{self.label_counter}"

    def _hex(self, v):
        return f"0x{v & 0xFFFF:04x}"

    def emit_add_const(self, reg, offset):
        """reg += offset （offsetはPythonのint、負数もサポート）"""
        if offset == 0:
            return []
        if offset > 0:
            return [f"    add {reg},{offset}"]
        return [f"    sub {reg},{-offset}"]

    def intern_string(self, text):
        if text in self.string_pool:
            return self.string_pool[text]
        label = f"__str_{len(self.string_pool)}"
        self.string_pool[text] = label
        return label

    def emit_syscall(self, num):
        # syscall命令はNC-16の仕様上bpレジスタを上書きする(成功時0/不正な
        # システムコール番号なら1)。bpは本コンパイラではフレームポインタとして
        # 使っているため、syscallの前後で必ず退避・復元する。
        return [
            "    push bp",
            f"    mov e,{num}",
            "    syscall",
            "    pop bp",
        ]

    # ---------------------------------------------------------------
    # トップレベル
    # ---------------------------------------------------------------
    def compile(self, program):
        # pass1: struct宣言を登録
        for d in program.decls:
            if isinstance(d, StructDecl):
                self._register_struct(d)

        # pass2: グローバル変数・関数シグネチャを登録（前方参照対応）
        for d in program.decls:
            if isinstance(d, FuncDecl):
                self._register_func_sig(d)
            elif isinstance(d, VarDecl):
                self._register_global(d)

        # pass3: 実際のコード生成
        for d in program.decls:
            if isinstance(d, FuncDecl):
                self._gen_func(d)
            elif isinstance(d, VarDecl):
                self._emit_global_data(d)

        return self._assemble()

    def _register_struct(self, sd):
        if sd.name in self.structs:
            raise CompileError(f"構造体が再定義されています: {sd.name}")
        fields = []
        offset = 0
        for tn, name, arr_len in sd.members:
            t = resolve_typename(tn, self.structs)
            if arr_len is not None:
                t = ArrayType(t, arr_len)
            fields.append((name, t, offset))
            offset += t.size()
        self.structs[sd.name] = StructType(sd.name, fields)

    def _register_func_sig(self, fd):
        if fd.name in self.funcs or fd.name in BUILTIN_SIGNATURES:
            raise CompileError(f"関数が再定義されています: {fd.name}")
        ret_type = None
        if not (fd.ret_typename.base_name == 'void' and fd.ret_typename.ptr_level == 0):
            ret_type = resolve_typename(fd.ret_typename, self.structs)
        params = [(name, resolve_typename(tn, self.structs)) for tn, name in fd.params]
        self.funcs[fd.name] = FuncSig(fd.name, ret_type, params)

    def _register_global(self, vd):
        if vd.name in self.globals:
            raise CompileError(f"グローバル変数が再定義されています: {vd.name}")
        t = resolve_typename(vd.typename, self.structs)
        if vd.array_len is not None:
            t = ArrayType(t, vd.array_len)
        label = f"g_{vd.name}"
        self.globals[vd.name] = Symbol(vd.name, t, 'global', label=label)

    def _emit_global_data(self, vd):
        sym = self.globals[vd.name]
        t = sym.type
        self.data_asm.append(f"{sym.label}:")
        if isinstance(t, (ArrayType, StructType)):
            if vd.init is not None:
                raise CompileError(f"配列/構造体型のグローバル変数の初期化はサポートしていません: {vd.name}")
            self.data_asm.append(f"    #res {t.size()}")
        else:
            val = 0
            if vd.init is not None:
                if not isinstance(vd.init, (Number, BoolLit)):
                    raise CompileError(f"グローバル変数の初期値には定数のみ使用できます: {vd.name}")
                val = vd.init.value if isinstance(vd.init, Number) else (1 if vd.init.value else 0)
            self.data_asm.append(f"    #d {self._hex(val)}")

    def _assemble(self):
        out = []
        out.append("; ============================================================")
        out.append("; このファイルは NC16C コンパイラによって自動生成されました。")
        out.append("; 手で編集する場合は再生成時に上書きされる点に注意してください。")
        out.append("; ============================================================")
        out.append('#include "nc16_assemble_USERPROGRAM.asm"')
        out.append("")
        out.append("program_start:")
        out.append("    call main")
        out.append("    userret")
        out.append("")
        out.append("; ---- 関数 ----")
        out.extend(self.func_asm)
        out.append("")
        out.append("; ---- グローバル変数 ----")
        out.extend(self.data_asm)
        if self.string_pool:
            out.append("")
            out.append("; ---- 文字列リテラル ----")
            for text, label in self.string_pool.items():
                escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
                out.append(f"{label}:")
                out.append(f'    #d "{escaped}\\0"')
                out.append("    #align 16")
        return "\n".join(out) + "\n"

    # ---------------------------------------------------------------
    # 関数コード生成
    # ---------------------------------------------------------------
    def _scan_locals(self, stmt, counter):
        if isinstance(stmt, VarDecl):
            t = resolve_typename(stmt.typename, self.structs)
            if stmt.array_len is not None:
                t = ArrayType(t, stmt.array_len)
            size = t.size()
            # 変数は size ワード分まとめて確保する。stmt.offset は先頭ワードの
            # bp相対オフセット（配列/構造体の場合、後続の要素は offset+1, offset+2,... に続く）
            stmt.offset = -(counter[0] + size)
            counter[0] += size
        elif isinstance(stmt, Block):
            for s in stmt.stmts:
                self._scan_locals(s, counter)
        elif isinstance(stmt, IfStmt):
            self._scan_locals(stmt.then_stmt, counter)
            if stmt.else_stmt:
                self._scan_locals(stmt.else_stmt, counter)
        elif isinstance(stmt, (WhileStmt, DoWhileStmt)):
            self._scan_locals(stmt.body, counter)
        elif isinstance(stmt, ForStmt):
            if stmt.init:
                self._scan_locals(stmt.init, counter)
            self._scan_locals(stmt.body, counter)
        elif isinstance(stmt, SwitchStmt):
            for _, stmts in stmt.cases:
                for s in stmts:
                    self._scan_locals(s, counter)
            if stmt.default:
                for s in stmt.default:
                    self._scan_locals(s, counter)

    def _gen_func(self, fd):
        sig = self.funcs[fd.name]
        self.cur_func_name = fd.name
        self.cur_ret_type = sig.ret_type

        scope = Scope()
        for i, (name, t) in enumerate(sig.params):
            scope.define(Symbol(name, t, 'param', offset=2 + i))

        counter = [0]
        self._scan_locals(fd.body, counter)
        total_locals = counter[0]

        epilogue = self.new_label(f"{fd.name}_end")
        self.cur_epilogue = epilogue

        out = [f"{fd.name}:", "    push bp", "    mov bp,sp"]
        if total_locals > 0:
            out.append(f"    sub sp,{total_locals}")
        out.extend(self._gen_stmt(fd.body, scope))
        out.append(f"{epilogue}:")
        out.append("    mov sp,bp")
        out.append("    pop bp")
        out.append("    ret")
        out.append("")
        self.func_asm.extend(out)

    # ---------------------------------------------------------------
    # 文コード生成
    # ---------------------------------------------------------------
    def _gen_stmt(self, stmt, scope):
        if isinstance(stmt, Block):
            inner = Scope(parent=scope)
            lines = []
            for s in stmt.stmts:
                lines.extend(self._gen_stmt(s, inner))
            return lines

        if isinstance(stmt, VarDecl):
            t = resolve_typename(stmt.typename, self.structs)
            if stmt.array_len is not None:
                t = ArrayType(t, stmt.array_len)
            sym = Symbol(stmt.name, t, 'local', offset=stmt.offset)
            scope.define(sym)
            lines = []
            if stmt.init is not None:
                if isinstance(t, (ArrayType, StructType)):
                    raise CompileError(f"配列/構造体型の初期化はサポートしていません: {stmt.name}")
                lines += self._gen_expr(stmt.init, scope)
                lines.append("    mov memval,a")
                lines.append("    mov a,bp")
                lines += self.emit_add_const('a', stmt.offset)
                lines.append("    mov memaddr,a")
                lines.append("    mov [memaddr+0],memval")
            return lines

        if isinstance(stmt, ExprStmt):
            return self._gen_expr(stmt.expr, scope)

        if isinstance(stmt, IfStmt):
            lines = self._gen_expr(stmt.cond, scope)
            lines.append("    cmp a,0")
            if stmt.else_stmt is None:
                Lend = self.new_label('if_end')
                lines.append(f"    je {Lend}")
                lines.extend(self._gen_stmt(stmt.then_stmt, scope))
                lines.append(f"{Lend}:")
            else:
                Lelse = self.new_label('else')
                Lend = self.new_label('if_end')
                lines.append(f"    je {Lelse}")
                lines.extend(self._gen_stmt(stmt.then_stmt, scope))
                lines.append(f"    jmp {Lend}")
                lines.append(f"{Lelse}:")
                lines.extend(self._gen_stmt(stmt.else_stmt, scope))
                lines.append(f"{Lend}:")
            return lines

        if isinstance(stmt, WhileStmt):
            Lstart = self.new_label('while')
            Lend = self.new_label('while_end')
            self.loop_labels.append((Lstart, Lend))
            lines = [f"{Lstart}:"]
            lines.extend(self._gen_expr(stmt.cond, scope))
            lines.append("    cmp a,0")
            lines.append(f"    je {Lend}")
            lines.extend(self._gen_stmt(stmt.body, scope))
            lines.append(f"    jmp {Lstart}")
            lines.append(f"{Lend}:")
            self.loop_labels.pop()
            return lines

        if isinstance(stmt, DoWhileStmt):
            Lstart = self.new_label('do')
            Lcontinue = self.new_label('do_cont')
            Lend = self.new_label('do_end')
            self.loop_labels.append((Lcontinue, Lend))
            lines = [f"{Lstart}:"]
            lines.extend(self._gen_stmt(stmt.body, scope))
            lines.append(f"{Lcontinue}:")
            lines.extend(self._gen_expr(stmt.cond, scope))
            lines.append("    cmp a,0")
            lines.append(f"    jne {Lstart}")
            lines.append(f"{Lend}:")
            self.loop_labels.pop()
            return lines

        if isinstance(stmt, ForStmt):
            inner = Scope(parent=scope)
            lines = []
            if stmt.init:
                lines.extend(self._gen_stmt(stmt.init, inner))
            Lstart = self.new_label('for')
            Lcontinue = self.new_label('for_cont')
            Lend = self.new_label('for_end')
            self.loop_labels.append((Lcontinue, Lend))
            lines.append(f"{Lstart}:")
            if stmt.cond:
                lines.extend(self._gen_expr(stmt.cond, inner))
                lines.append("    cmp a,0")
                lines.append(f"    je {Lend}")
            lines.extend(self._gen_stmt(stmt.body, inner))
            lines.append(f"{Lcontinue}:")
            if stmt.step:
                lines.extend(self._gen_expr(stmt.step, inner))
            lines.append(f"    jmp {Lstart}")
            lines.append(f"{Lend}:")
            self.loop_labels.pop()
            return lines

        if isinstance(stmt, SwitchStmt):
            return self._gen_switch(stmt, scope)

        if isinstance(stmt, BreakStmt):
            if self.switch_break_labels:
                return [f"    jmp {self.switch_break_labels[-1]}"]
            if self.loop_labels:
                return [f"    jmp {self.loop_labels[-1][1]}"]
            raise CompileError("break文がループ/switch文の外で使用されています")

        if isinstance(stmt, ContinueStmt):
            if not self.loop_labels:
                raise CompileError("continue文がループの外で使用されています")
            return [f"    jmp {self.loop_labels[-1][0]}"]

        if isinstance(stmt, ReturnStmt):
            lines = []
            if stmt.expr is not None:
                lines.extend(self._gen_expr(stmt.expr, scope))
            lines.append(f"    jmp {self.cur_epilogue}")
            return lines

        raise CompileError(f"未対応の文です: {stmt}")

    def _gen_switch(self, stmt, scope):
        # switch(expr) { case V: ...; default: ...; } は、比較の連鎖(if-elif chain)として展開する。
        # 本実装ではC言語同様、break文が無い限り次のcaseへフォールスルーする。
        lines = self._gen_expr(stmt.expr, scope)
        lines.append("    push a")

        Lend = self.new_label('switch_end')
        self.switch_break_labels.append(Lend)

        case_labels = []
        for value, _ in stmt.cases:
            case_labels.append(self.new_label(f'case_{value}'))
        default_label = self.new_label('default') if stmt.default is not None else Lend

        # 比較チェーン
        for (value, _), clabel in zip(stmt.cases, case_labels):
            lines.append("    mov memaddr,sp")
            lines.append("    mov a,[memaddr+0]")
            lines.append(f"    cmp a,{value & 0xFFFF}")
            lines.append(f"    je {clabel}")
        lines.append(f"    jmp {default_label}")

        # 各case本体
        for (value, body), clabel in zip(stmt.cases, case_labels):
            lines.append(f"{clabel}:")
            for s in body:
                lines.extend(self._gen_stmt(s, scope))

        if stmt.default is not None:
            lines.append(f"{default_label}:")
            for s in stmt.default:
                lines.extend(self._gen_stmt(s, scope))

        lines.append(f"{Lend}:")
        lines.append("    add sp,1")  # push しておいたswitch対象の値を捨てる
        self.switch_break_labels.pop()
        return lines

    # ---------------------------------------------------------------
    # 型推論
    # ---------------------------------------------------------------
    def _infer_type(self, node, scope):
        if isinstance(node, Number):
            return UINT
        if isinstance(node, BoolLit):
            return BOOL
        if isinstance(node, StringLit):
            return PointerType(CHAR)
        if isinstance(node, Ident):
            sym = scope.lookup(node.name) if scope else None
            if sym is None:
                sym = self.globals.get(node.name)
            if sym is None:
                raise CompileError(f"未定義の変数です: {node.name}")
            return sym.type
        if isinstance(node, Index):
            t = self._infer_type(node.base, scope)
            if not is_ptr_like(t):
                raise CompileError("配列またはポインタ以外に添字アクセスしています")
            return t.base
        if isinstance(node, Member):
            bt = self._infer_type(node.base, scope)
            if node.is_arrow:
                if not isinstance(bt, PointerType):
                    raise CompileError("-> はポインタに対してのみ使用できます")
                bt = bt.base
            if not isinstance(bt, StructType):
                raise CompileError(". は構造体に対してのみ使用できます")
            ftype, _ = bt.field(node.name)
            if ftype is None:
                raise CompileError(f"構造体 {bt.name} にメンバ {node.name} は存在しません")
            return ftype
        if isinstance(node, Deref):
            t = self._infer_type(node.operand, scope)
            if not isinstance(t, PointerType):
                raise CompileError("* はポインタに対してのみ使用できます")
            return t.base
        if isinstance(node, AddrOf):
            return PointerType(self._infer_type(node.operand, scope))
        if isinstance(node, UnaryOp):
            if node.op == '!':
                return BOOL
            return self._infer_type(node.operand, scope)
        if isinstance(node, BinOp):
            if node.op in ('==', '!=', '<', '<=', '>', '>=', '&&', '||'):
                return BOOL
            lt = self._infer_type(node.left, scope)
            rt = self._infer_type(node.right, scope)
            if is_ptr_like(lt):
                return lt if not isinstance(lt, ArrayType) else PointerType(lt.base)
            if is_ptr_like(rt):
                return rt if not isinstance(rt, ArrayType) else PointerType(rt.base)
            return UINT
        if isinstance(node, Assign):
            return self._infer_type(node.target, scope)
        if isinstance(node, Call):
            if node.name in BUILTIN_SIGNATURES:
                return BUILTIN_SIGNATURES[node.name].ret_type
            if node.name in self.funcs:
                return self.funcs[node.name].ret_type or UINT
            raise CompileError(f"未定義の関数です: {node.name}")
        raise CompileError(f"型を推論できません: {node}")

    # ---------------------------------------------------------------
    # アドレス計算（lvalue）: レジスタaに対象のメモリ番地を残す
    # 戻り値: (行リスト, その場所に格納されている値の型)
    # ---------------------------------------------------------------
    def _gen_addr(self, node, scope):
        if isinstance(node, Ident):
            sym = scope.lookup(node.name) if scope else None
            if sym is None:
                sym = self.globals.get(node.name)
            if sym is None:
                raise CompileError(f"未定義の変数です: {node.name}")
            if sym.kind == 'global':
                return [f"    mov a,{sym.label}"], sym.type
            lines = ["    mov a,bp"] + self.emit_add_const('a', sym.offset)
            return lines, sym.type

        if isinstance(node, Index):
            bt = self._infer_type(node.base, scope)
            if isinstance(bt, ArrayType):
                base_lines, _ = self._gen_addr(node.base, scope)
                elem_type = bt.base
            elif isinstance(bt, PointerType):
                base_lines = self._gen_expr(node.base, scope)
                elem_type = bt.base
            else:
                raise CompileError("配列またはポインタ以外に添字アクセスしています")
            lines = list(base_lines)
            lines.append("    push a")
            lines += self._gen_expr(node.index, scope)
            if elem_type.size() != 1:
                lines.append(f"    mul a,{elem_type.size()}")
            lines.append("    mov b,a")
            lines.append("    pop a")
            lines.append("    add a,b")
            return lines, elem_type

        if isinstance(node, Member):
            bt = self._infer_type(node.base, scope)
            if node.is_arrow:
                if not isinstance(bt, PointerType):
                    raise CompileError("-> はポインタに対してのみ使用できます")
                base_lines = self._gen_expr(node.base, scope)
                struct_t = bt.base
            else:
                base_lines, base_t = self._gen_addr(node.base, scope)
                struct_t = base_t
            if not isinstance(struct_t, StructType):
                raise CompileError(". / -> は構造体に対してのみ使用できます")
            ftype, foff = struct_t.field(node.name)
            if ftype is None:
                raise CompileError(f"構造体 {struct_t.name} にメンバ {node.name} は存在しません")
            lines = list(base_lines) + self.emit_add_const('a', foff)
            return lines, ftype

        if isinstance(node, Deref):
            t = self._infer_type(node.operand, scope)
            if not isinstance(t, PointerType):
                raise CompileError("* はポインタに対してのみ使用できます")
            lines = self._gen_expr(node.operand, scope)
            return lines, t.base

        raise CompileError(f"代入可能な式（lvalue）ではありません: {node}")

    # ---------------------------------------------------------------
    # 式コード生成: レジスタaに結果を残す
    # ---------------------------------------------------------------
    def _gen_expr(self, node, scope):
        if isinstance(node, (Ident, Index, Member, Deref)):
            addr_lines, t = self._gen_addr(node, scope)
            if isinstance(t, ArrayType):
                return addr_lines  # 配列は先頭アドレスへdecayする
            return addr_lines + ["    mov memaddr,a", "    mov a,[memaddr+0]"]

        if isinstance(node, Number):
            return [f"    mov a,{self._hex(node.value)}"]

        if isinstance(node, BoolLit):
            return [f"    mov a,{1 if node.value else 0}"]

        if isinstance(node, StringLit):
            label = self.intern_string(node.value)
            return [f"    mov a,{label}"]

        if isinstance(node, AddrOf):
            lines, _ = self._gen_addr(node.operand, scope)
            return lines

        if isinstance(node, Assign):
            addr_lines, target_type = self._gen_addr(node.target, scope)
            lines = list(addr_lines)
            lines.append("    push a")
            lines += self._gen_expr(node.value, scope)
            lines.append("    mov memval,a")
            lines.append("    pop a")
            lines.append("    mov memaddr,a")
            lines.append("    mov [memaddr+0],memval")
            lines.append("    mov a,memval")
            return lines

        if isinstance(node, UnaryOp):
            return self._gen_unary(node, scope)

        if isinstance(node, BinOp):
            return self._gen_binop(node, scope)

        if isinstance(node, Call):
            return self._gen_call(node, scope)

        raise CompileError(f"未対応の式です: {node}")

    def _gen_unary(self, node, scope):
        if node.op == '-':
            lines = self._gen_expr(node.operand, scope)
            lines.append("    mov b,a")
            lines.append("    mov a,0")
            lines.append("    sub a,b")
            return lines
        if node.op == '~':
            lines = self._gen_expr(node.operand, scope)
            lines.append("    not a")
            return lines
        if node.op == '!':
            lines = self._gen_expr(node.operand, scope)
            Lfalse = self.new_label('not_false')
            Lend = self.new_label('not_end')
            lines.append("    cmp a,0")
            lines.append(f"    jne {Lfalse}")
            lines.append("    mov a,1")
            lines.append(f"    jmp {Lend}")
            lines.append(f"{Lfalse}:")
            lines.append("    mov a,0")
            lines.append(f"{Lend}:")
            return lines
        raise CompileError(f"未対応の単項演算子です: {node.op}")

    def _gen_binop(self, node, scope):
        op = node.op
        if op == '&&':
            return self._gen_logical_and(node, scope)
        if op == '||':
            return self._gen_logical_or(node, scope)
        if op in ('==', '!=', '<', '<=', '>', '>='):
            return self._gen_relational(node, scope)
        if op == '/':
            return self._gen_divmod(node, scope, want_remainder=False)
        if op == '%':
            return self._gen_divmod(node, scope, want_remainder=True)
        if op == '<<':
            return self._gen_shift_left(node, scope)

        lt = self._infer_type(node.left, scope)
        rt = self._infer_type(node.right, scope)
        lines = self._gen_expr(node.left, scope)
        lines.append("    push a")
        lines += self._gen_expr(node.right, scope)
        lines.append("    mov b,a")
        lines.append("    pop a")

        if op in ('+', '-'):
            if is_ptr_like(lt) and not is_ptr_like(rt):
                esz = lt.base.size()
                if esz != 1:
                    lines.append(f"    mul b,{esz}")
            elif op == '+' and is_ptr_like(rt) and not is_ptr_like(lt):
                esz = rt.base.size()
                if esz != 1:
                    lines.append(f"    mul a,{esz}")
            lines.append(f"    {'add' if op == '+' else 'sub'} a,b")
            return lines

        opmap = {'*': 'mul', '&': 'and', '|': 'or', '^': 'xor'}
        if op in opmap:
            lines.append(f"    {opmap[op]} a,b")
            return lines
        if op == '>>':
            lines.append("    shr a,b")
            return lines

        raise CompileError(f"未対応の二項演算子です: {op}")

    def _gen_logical_and(self, node, scope):
        Lfalse = self.new_label('and_false')
        Lend = self.new_label('and_end')
        lines = self._gen_expr(node.left, scope)
        lines.append("    cmp a,0")
        lines.append(f"    je {Lfalse}")
        lines += self._gen_expr(node.right, scope)
        lines.append("    cmp a,0")
        lines.append(f"    je {Lfalse}")
        lines.append("    mov a,1")
        lines.append(f"    jmp {Lend}")
        lines.append(f"{Lfalse}:")
        lines.append("    mov a,0")
        lines.append(f"{Lend}:")
        return lines

    def _gen_logical_or(self, node, scope):
        Ltrue = self.new_label('or_true')
        Lend = self.new_label('or_end')
        lines = self._gen_expr(node.left, scope)
        lines.append("    cmp a,0")
        lines.append(f"    jne {Ltrue}")
        lines += self._gen_expr(node.right, scope)
        lines.append("    cmp a,0")
        lines.append(f"    jne {Ltrue}")
        lines.append("    mov a,0")
        lines.append(f"    jmp {Lend}")
        lines.append(f"{Ltrue}:")
        lines.append("    mov a,1")
        lines.append(f"{Lend}:")
        return lines

    def _gen_relational(self, node, scope):
        # NC-16のjl/jle/ja/jaeは符号フラグのみで判定されるため、素の状態では
        # 符号付き比較になってしまう。uintの0～65535全域で正しく比較するため、
        # 両オペランドの最上位ビットをxor 0x8000で反転させてから比較する。
        # （このビット反転は大小関係の順序を保つ）
        op = node.op
        lines = self._gen_expr(node.left, scope)
        lines.append("    push a")
        lines += self._gen_expr(node.right, scope)
        lines.append("    mov b,a")
        lines.append("    pop a")

        if op in ('<', '<=', '>', '>='):
            lines.append("    xor a,0x8000")
            lines.append("    xor b,0x8000")

        lines.append("    cmp a,b")
        jmp_true = {'==': 'je', '!=': 'jne', '<': 'jl', '<=': 'jle', '>': 'ja', '>=': 'jae'}[op]
        Ltrue = self.new_label('rel_true')
        Lend = self.new_label('rel_end')
        lines.append(f"    {jmp_true} {Ltrue}")
        lines.append("    mov a,0")
        lines.append(f"    jmp {Lend}")
        lines.append(f"{Ltrue}:")
        lines.append("    mov a,1")
        lines.append(f"{Lend}:")
        return lines

    def _gen_divmod(self, node, scope, want_remainder):
        # NC-16には除算命令が無いため、MomoOSのdivideシステムコール(復元法による
        # 二進除算、番号6)を直接呼び出す。商はcレジスタ、余りはdレジスタに返る。
        # ゼロ除算の場合は商・余りともに0になる（言語仕様として定義：GRAMMAR.md参照）。
        lines = self._gen_expr(node.left, scope)
        lines.append("    push a")
        lines += self._gen_expr(node.right, scope)
        lines.append("    mov b,a")
        lines.append("    pop a")
        lines.extend(self.emit_syscall(6))
        lines.append(f"    mov a,{'d' if want_remainder else 'c'}")
        return lines

    def _gen_shift_left(self, node, scope):
        # NC-16には左シフト命令が無いため、加算(自己加算=2倍)をシフト量の回数だけ
        # 繰り返すループで代用する。
        lines = self._gen_expr(node.left, scope)
        lines.append("    push a")
        lines += self._gen_expr(node.right, scope)
        lines.append("    mov b,a")
        lines.append("    pop a")
        Lloop = self.new_label('shl')
        Lend = self.new_label('shl_end')
        lines.append(f"{Lloop}:")
        lines.append("    cmp b,0")
        lines.append(f"    je {Lend}")
        lines.append("    add a,a")
        lines.append("    sub b,1")
        lines.append(f"    jmp {Lloop}")
        lines.append(f"{Lend}:")
        return lines

    # ---------------------------------------------------------------
    # 関数呼び出し
    # ---------------------------------------------------------------
    def _gen_call(self, node, scope):
        if node.name in BUILTIN_SIGNATURES:
            return self._gen_builtin_call(node, scope)
        if node.name not in self.funcs:
            raise CompileError(f"未定義の関数です: {node.name}")
        sig = self.funcs[node.name]
        if len(node.args) != len(sig.params):
            raise CompileError(
                f"関数 {node.name} の引数の数が一致しません（期待:{len(sig.params)} 実際:{len(node.args)}）")

        lines = []
        # 呼び出し規約: 引数は「右から左」の順にpushする（cdecl方式）。
        # こうすることで、call後にbpから見て bp+2 が第1引数、bp+3 が第2引数、
        # ...という並びになる（最後にpushされた第1引数がretaddrに一番近い位置に来るため）。
        for a in reversed(node.args):
            lines.extend(self._gen_expr(a, scope))
            lines.append("    push a")
        lines.append(f"    call {node.name}")
        if len(node.args) > 0:
            lines.append(f"    add sp,{len(node.args)}")
        return lines

    def _gen_builtin_call(self, node, scope):
        sig = BUILTIN_SIGNATURES[node.name]
        if len(node.args) != len(sig.params):
            raise CompileError(
                f"組み込み関数 {node.name} の引数の数が一致しません"
                f"（期待:{len(sig.params)} 実際:{len(node.args)}）")
        method = getattr(self, f"_builtin_{node.name}")
        return method(node.args, scope)

    def _load_args_to_regs(self, args, regs, scope):
        """args[i] を評価し、最終的に regs[i] （文字列のレジスタ名リスト）に格納する"""
        lines = []
        for a in args:
            lines.extend(self._gen_expr(a, scope))
            lines.append("    push a")
        for r in reversed(regs):
            lines.append(f"    pop {r}")
        return lines

    def _builtin_input_user_string(self, args, scope):
        lines = self._load_args_to_regs(args, ['a'], scope)
        lines.extend(self.emit_syscall(0))
        lines.append("    mov a,b")
        return lines

    def _builtin_compare_to_string(self, args, scope):
        lines = self._load_args_to_regs(args, ['a', 'b'], scope)
        lines.extend(self.emit_syscall(1))
        lines.append("    mov a,c")
        return lines

    def _builtin_read_rom_data(self, args, scope):
        lines = self._load_args_to_regs(args, ['a', 'b', 'c', 'd'], scope)
        lines.extend(self.emit_syscall(2))
        lines.append("    mov a,e")
        return lines

    def _builtin_output_string(self, args, scope):
        lines = self._load_args_to_regs(args, ['b'], scope)
        lines.extend(self.emit_syscall(3))
        lines.append("    mov a,c")
        return lines

    def _builtin_ascii_to_int(self, args, scope):
        # 第2引数(out_value)はポインタ。先にアドレスを評価してpushしておき、
        # syscall完了後にそのアドレスへ結果(bレジスタ)を書き込む。
        str_expr, out_ptr_expr = args
        lines = self._gen_expr(out_ptr_expr, scope)
        lines.append("    push a")
        lines += self._gen_expr(str_expr, scope)
        lines.extend(self.emit_syscall(4))
        # ここで b=変換値, c=処理結果
        lines.append("    pop d")           # d = out_valueのアドレス
        lines.append("    mov memaddr,d")
        lines.append("    mov memval,b")
        lines.append("    mov [memaddr+0],memval")
        lines.append("    mov a,c")
        return lines

    def _builtin_int_to_ascii(self, args, scope):
        lines = self._load_args_to_regs(args, ['a', 'b'], scope)
        lines.extend(self.emit_syscall(5))
        lines.append("    mov a,c")
        return lines

    def _builtin_divide(self, args, scope):
        dividend_expr, divisor_expr, rem_ptr_expr, status_ptr_expr = args
        lines = self._gen_expr(rem_ptr_expr, scope)
        lines.append("    push a")
        lines += self._gen_expr(status_ptr_expr, scope)
        lines.append("    push a")
        lines += self._load_args_to_regs([dividend_expr, divisor_expr], ['a', 'b'], scope)
        lines.extend(self.emit_syscall(6))
        # c=商, d=余り, e=状態
        lines.append("    pop a")   # a = status_ptrのアドレス
        lines.append("    pop b")   # b = remainder_ptrのアドレス
        lines.append("    mov memaddr,b")
        lines.append("    mov memval,d")
        lines.append("    mov [memaddr+0],memval")
        lines.append("    mov memaddr,a")
        lines.append("    mov memval,e")
        lines.append("    mov [memaddr+0],memval")
        lines.append("    mov a,c")
        return lines

    def _builtin_random(self,args,scope):
        lines = []
        lines.extend(self.emit_syscall(7))
        return lines
        
        


def generate(program):
    cg = CodeGen()
    return cg.compile(program)
