# -*- coding: utf-8 -*-
"""
NC16C 構文解析器 (parser)
ply.yacc を使用し、トークン列からASTを構築する。
"""
import ply.yacc as yacc
from lexer import tokens, build_lexer
from ast_nodes import *

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'BITOR'),
    ('left', 'BITXOR'),
    ('left', 'BITAND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'SHL', 'SHR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH', 'PERCENT'),
    ('right', 'UNARY'),
    ('left', 'LBRACKET', 'LPAREN', 'DOT', 'ARROW'),
)


# ============================================================
# トップレベル
# ============================================================
def p_program(p):
    'program : decl_list'
    p[0] = Program(p[1])


def p_decl_list(p):
    '''decl_list : decl_list decl
                  | decl'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_decl(p):
    '''decl : struct_decl
            | func_or_var_decl'''
    p[0] = p[1]


def p_struct_decl(p):
    'struct_decl : STRUCT IDENT LBRACE member_list RBRACE SEMI'
    p[0] = StructDecl(p[2], p[4])


def p_member_list(p):
    '''member_list : member_list member_decl
                    | member_decl'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_member_decl(p):
    'member_decl : type IDENT array_opt SEMI'
    p[0] = (p[1], p[2], p[3])


def p_array_opt(p):
    '''array_opt : LBRACKET NUMBER RBRACKET
                 | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = None


def p_func_or_var_decl(p):
    '''func_or_var_decl : type IDENT LPAREN param_list_opt RPAREN block
                         | type IDENT array_opt init_opt SEMI'''
    if len(p) == 7:
        p[0] = FuncDecl(p[1], p[2], p[4], p[6])
    else:
        p[0] = VarDecl(p[1], p[2], p[3], p[4])


def p_init_opt(p):
    '''init_opt : ASSIGN expr
                | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_param_list_opt(p):
    '''param_list_opt : param_list
                       | VOID
                       | empty'''
    if p[1] == 'void' or p[1] is None:
        p[0] = []
    else:
        p[0] = p[1]


def p_param_list(p):
    '''param_list : param_list COMMA param
                   | param'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_param(p):
    'param : type IDENT array_opt'
    # 配列パラメータはポインタとして扱う（C言語と同様の減衰）
    tn = p[1]
    if p[3] is not None:
        tn = TypeName(tn.base_name, tn.ptr_level + 1)
    p[0] = (tn, p[2])


# ============================================================
# 型
# ============================================================
def p_type(p):
    'type : type_base stars'
    p[0] = TypeName(p[1], p[2])


def p_type_base(p):
    '''type_base : CHAR
                  | BOOL
                  | UINT
                  | STRUCT IDENT'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_stars(p):
    '''stars : stars STAR
             | empty'''
    if len(p) == 3:
        p[0] = p[1] + 1
    else:
        p[0] = 0


def p_empty(p):
    'empty :'
    p[0] = None


# ============================================================
# 文
# ============================================================
def p_block(p):
    'block : LBRACE stmt_list RBRACE'
    p[0] = Block(p[2])


def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_stmt(p):
    '''stmt : var_decl_stmt
            | expr_stmt
            | if_stmt
            | while_stmt
            | do_while_stmt
            | for_stmt
            | switch_stmt
            | break_stmt
            | continue_stmt
            | return_stmt
            | block'''
    p[0] = p[1]


def p_var_decl_stmt(p):
    'var_decl_stmt : type IDENT array_opt init_opt SEMI'
    p[0] = VarDecl(p[1], p[2], p[3], p[4])


def p_expr_stmt(p):
    'expr_stmt : expr SEMI'
    p[0] = ExprStmt(p[1])


def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN stmt ELSE stmt
               | IF LPAREN expr RPAREN stmt'''
    if len(p) == 8:
        p[0] = IfStmt(p[3], p[5], p[7])
    else:
        p[0] = IfStmt(p[3], p[5], None)


def p_while_stmt(p):
    'while_stmt : WHILE LPAREN expr RPAREN stmt'
    p[0] = WhileStmt(p[3], p[5])


def p_do_while_stmt(p):
    'do_while_stmt : DO stmt WHILE LPAREN expr RPAREN SEMI'
    p[0] = DoWhileStmt(p[2], p[5])


def p_for_stmt(p):
    'for_stmt : FOR LPAREN for_init expr_opt SEMI expr_opt RPAREN stmt'
    p[0] = ForStmt(p[3], p[4], p[6], p[8])


def p_for_init(p):
    '''for_init : var_decl_stmt
                | expr_stmt
                | SEMI'''
    if p[1] == ';':
        p[0] = None
    else:
        p[0] = p[1]


def p_expr_opt(p):
    '''expr_opt : expr
                | empty'''
    p[0] = p[1]


def p_switch_stmt(p):
    'switch_stmt : SWITCH LPAREN expr RPAREN LBRACE case_list default_opt RBRACE'
    p[0] = SwitchStmt(p[3], p[6], p[7])


def p_case_list(p):
    '''case_list : case_list case_clause
                 | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_case_clause(p):
    'case_clause : CASE NUMBER COLON stmt_list'
    p[0] = (p[2], p[4])


def p_default_opt(p):
    '''default_opt : DEFAULT COLON stmt_list
                    | empty'''
    if len(p) == 4:
        p[0] = p[3]
    else:
        p[0] = None


def p_break_stmt(p):
    'break_stmt : BREAK SEMI'
    p[0] = BreakStmt()


def p_continue_stmt(p):
    'continue_stmt : CONTINUE SEMI'
    p[0] = ContinueStmt()


def p_return_stmt(p):
    '''return_stmt : RETURN expr SEMI
                    | RETURN SEMI'''
    if len(p) == 4:
        p[0] = ReturnStmt(p[2])
    else:
        p[0] = ReturnStmt(None)


# ============================================================
# 式
# ============================================================
def p_expr_assign(p):
    'expr : unary ASSIGN expr'
    p[0] = Assign(p[1], p[3])


def p_expr_plusassign(p):
    '''expr : unary PLUSEQ expr
            | unary MINUSEQ expr'''
    op = '+' if p[2] == '+=' else '-'
    p[0] = Assign(p[1], BinOp(op, p[1], p[3]))


def p_expr_binop(p):
    '''expr : expr OR expr
            | expr AND expr
            | expr BITOR expr
            | expr BITXOR expr
            | expr BITAND expr
            | expr EQ expr
            | expr NE expr
            | expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr SHL expr
            | expr SHR expr
            | expr PLUS expr
            | expr MINUS expr
            | expr STAR expr
            | expr SLASH expr
            | expr PERCENT expr'''
    p[0] = BinOp(p[2], p[1], p[3])


def p_expr_unary_group(p):
    'expr : unary'
    p[0] = p[1]


def p_unary_postfix(p):
    'unary : postfix'
    p[0] = p[1]


def p_unary_ops(p):
    '''unary : MINUS unary %prec UNARY
             | NOT unary %prec UNARY
             | BITNOT unary %prec UNARY
             | STAR unary %prec UNARY
             | BITAND unary %prec UNARY'''
    if p[1] == '-':
        p[0] = UnaryOp('-', p[2])
    elif p[1] == '!':
        p[0] = UnaryOp('!', p[2])
    elif p[1] == '~':
        p[0] = UnaryOp('~', p[2])
    elif p[1] == '*':
        p[0] = Deref(p[2])
    elif p[1] == '&':
        p[0] = AddrOf(p[2])


def p_unary_preincdec(p):
    '''unary : PLUSPLUS unary %prec UNARY
             | MINUSMINUS unary %prec UNARY'''
    op = '+' if p[1] == '++' else '-'
    p[0] = Assign(p[2], BinOp(op, p[2], Number(1)))


def p_postfix_incdec(p):
    '''postfix : postfix PLUSPLUS
               | postfix MINUSMINUS'''
    # x++ は「評価順は無視して x=x+1 の結果を返す」という簡略化されたセマンティクスとする
    # （後置と前置の値の違いは厳密には区別しない。詳細はGRAMMAR.md参照）
    op = '+' if p[2] == '++' else '-'
    p[0] = Assign(p[1], BinOp(op, p[1], Number(1)))


def p_postfix_index(p):
    'postfix : postfix LBRACKET expr RBRACKET'
    p[0] = Index(p[1], p[3])


def p_postfix_call(p):
    'postfix : IDENT LPAREN arg_list_opt RPAREN'
    p[0] = Call(p[1], p[3])


def p_postfix_member(p):
    'postfix : postfix DOT IDENT'
    p[0] = Member(p[1], p[3], False)


def p_postfix_arrow(p):
    'postfix : postfix ARROW IDENT'
    p[0] = Member(p[1], p[3], True)


def p_postfix_primary(p):
    'postfix : primary'
    p[0] = p[1]


def p_arg_list_opt(p):
    '''arg_list_opt : arg_list
                     | empty'''
    p[0] = p[1] if p[1] is not None else []


def p_arg_list(p):
    '''arg_list : arg_list COMMA expr
                | expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_primary_number(p):
    'primary : NUMBER'
    p[0] = Number(p[1])


def p_primary_charlit(p):
    'primary : CHARLIT'
    p[0] = Number(p[1])


def p_primary_true(p):
    'primary : TRUE'
    p[0] = BoolLit(True)


def p_primary_false(p):
    'primary : FALSE'
    p[0] = BoolLit(False)


def p_primary_string(p):
    'primary : STRINGLIT'
    p[0] = StringLit(p[1])


def p_primary_ident(p):
    'primary : IDENT'
    p[0] = Ident(p[1])


def p_primary_paren(p):
    'primary : LPAREN expr RPAREN'
    p[0] = p[2]


def p_error(p):
    if p is None:
        raise SyntaxError("構文エラー: 予期しないファイル終端です")
    raise SyntaxError(f"構文エラー: 予期しないトークン {p.type}={p.value!r} (行 {p.lineno})")


def build_parser(**kwargs):
    return yacc.yacc(**kwargs)


def parse(src, debug=False):
    lexer = build_lexer()
    parser = build_parser(debug=debug)
    return parser.parse(src, lexer=lexer)
