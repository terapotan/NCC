# -*- coding: utf-8 -*-
"""
NC16C 型システム・シンボルテーブル。

NC-16はワードアドレッシング（1アドレス=1ワード=16bit）のマシンであるため、
本コンパイラでは char / bool / uint / ポインタ をすべて「1ワード」として扱う。
（実際のC言語のようなバイト単位のアドレッシングは行わない。詳細はGRAMMAR.md参照）
"""


class CompileError(Exception):
    pass


# ---- 型 ----
class Type:
    def size(self):
        raise NotImplementedError

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))


class PrimType(Type):
    def __init__(self, name):
        self.name = name  # 'char' | 'bool' | 'uint'

    def size(self):
        return 1

    def __repr__(self):
        return self.name


class PointerType(Type):
    def __init__(self, base):
        self.base = base

    def size(self):
        return 1

    def __repr__(self):
        return f"{self.base}*"


class ArrayType(Type):
    def __init__(self, base, length):
        self.base = base
        self.length = length

    def size(self):
        return self.base.size() * self.length

    def __repr__(self):
        return f"{self.base}[{self.length}]"


class StructType(Type):
    def __init__(self, name, fields=None):
        self.name = name
        # fields: list of (fieldname, Type, offset)
        self.fields = fields if fields is not None else []
        self._size = None

    def size(self):
        if self._size is None:
            self._size = sum(t.size() for _, t, _ in self.fields)
        return self._size

    def field(self, name):
        for fname, ftype, off in self.fields:
            if fname == name:
                return ftype, off
        return None, None

    def __repr__(self):
        return f"struct {self.name}"


UINT = PrimType('uint')
CHAR = PrimType('char')
BOOL = PrimType('bool')


class Symbol:
    def __init__(self, name, type_, kind, offset=None, label=None):
        self.name = name
        self.type = type_
        self.kind = kind  # 'global' | 'local' | 'param'
        self.offset = offset  # local/paramの場合、bp相対オフセット(word単位)
        self.label = label  # globalの場合、アセンブリ上のラベル名


class FuncSig:
    def __init__(self, name, ret_type, params):
        self.name = name
        self.ret_type = ret_type
        self.params = params  # list of (name, Type)


class Scope:
    """関数内のブロックスコープ（変数名解決用）"""
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def define(self, sym):
        self.symbols[sym.name] = sym

    def lookup(self, name):
        s = self
        while s is not None:
            if name in s.symbols:
                return s.symbols[name]
            s = s.parent
        return None


def resolve_typename(tn, structs):
    """ast_nodes.TypeName -> symtab.Type に変換する"""
    base_name = tn.base_name
    if base_name == 'char':
        base = CHAR
    elif base_name == 'bool':
        base = BOOL
    elif base_name == 'uint':
        base = UINT
    elif base_name in structs:
        base = structs[base_name]
    else:
        raise CompileError(f"未定義の型です: {base_name}")
    t = base
    for _ in range(tn.ptr_level):
        t = PointerType(t)
    return t
