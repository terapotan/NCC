# -*- coding: utf-8 -*-
"""
NC16C AST（抽象構文木）ノード定義。
すべてシンプルなクラスとして定義し、フィールドにパース結果を保持する。
"""


class Node:
    def __repr__(self):
        fields = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"


# ---- 型 ----
class TypeName(Node):
    """パーサ段階での型表記。base_name('char'/'bool'/'uint'/構造体名) + ptr_level(*の数)"""
    def __init__(self, base_name, ptr_level=0):
        self.base_name = base_name
        self.ptr_level = ptr_level


# ---- トップレベル宣言 ----
class Program(Node):
    def __init__(self, decls):
        self.decls = decls


class StructDecl(Node):
    def __init__(self, name, members):
        self.name = name
        self.members = members  # list of (TypeName, name, array_len_or_None)


class VarDecl(Node):
    def __init__(self, typename, name, array_len, init):
        self.typename = typename
        self.name = name
        self.array_len = array_len  # None または int
        self.init = init  # None または式


class FuncDecl(Node):
    def __init__(self, ret_typename, name, params, body):
        self.ret_typename = ret_typename
        self.name = name
        self.params = params  # list of (TypeName, name)
        self.body = body  # Block


# ---- 文 ----
class Block(Node):
    def __init__(self, stmts):
        self.stmts = stmts


class ExprStmt(Node):
    def __init__(self, expr):
        self.expr = expr


class IfStmt(Node):
    def __init__(self, cond, then_stmt, else_stmt):
        self.cond = cond
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt


class WhileStmt(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class DoWhileStmt(Node):
    def __init__(self, body, cond):
        self.body = body
        self.cond = cond


class ForStmt(Node):
    def __init__(self, init, cond, step, body):
        self.init = init  # VarDecl / ExprStmt / None
        self.cond = cond  # 式 or None
        self.step = step  # 式 or None
        self.body = body


class SwitchStmt(Node):
    def __init__(self, expr, cases, default):
        self.expr = expr
        self.cases = cases  # list of (value:int, stmts:list)
        self.default = default  # stmts list または None


class BreakStmt(Node):
    pass


class ContinueStmt(Node):
    pass


class ReturnStmt(Node):
    def __init__(self, expr):
        self.expr = expr


# ---- 式 ----
class Number(Node):
    def __init__(self, value):
        self.value = value


class BoolLit(Node):
    def __init__(self, value):
        self.value = value  # True/False


class StringLit(Node):
    def __init__(self, value):
        self.value = value


class Ident(Node):
    def __init__(self, name):
        self.name = name


class Assign(Node):
    def __init__(self, target, value):
        self.target = target
        self.value = value


class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class AddrOf(Node):
    def __init__(self, operand):
        self.operand = operand


class Deref(Node):
    def __init__(self, operand):
        self.operand = operand


class Index(Node):
    def __init__(self, base, index):
        self.base = base
        self.index = index


class Member(Node):
    def __init__(self, base, name, is_arrow):
        self.base = base
        self.name = name
        self.is_arrow = is_arrow


class Call(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args
