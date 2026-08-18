# -*- coding: utf-8 -*-
"""
NC16C 字句解析器 (lexer)
NC-16向けのC風言語「NC16C」のトークナイザ。ply.lex を使用する。
"""
import ply.lex as lex

keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'do': 'DO',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'struct': 'STRUCT',
    'char': 'CHAR',
    'bool': 'BOOL',
    'uint': 'UINT',
    'void': 'VOID',
    'true': 'TRUE',
    'false': 'FALSE',
}

tokens = [
    'IDENT', 'NUMBER', 'CHARLIT', 'STRINGLIT',
    'PLUS', 'MINUS', 'STAR', 'SLASH', 'PERCENT',
    'ASSIGN',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'AND', 'OR', 'NOT',
    'BITAND', 'BITOR', 'BITXOR', 'BITNOT',
    'SHL', 'SHR',
    'PLUSPLUS', 'MINUSMINUS',
    'PLUSEQ', 'MINUSEQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMI', 'COMMA', 'DOT', 'ARROW', 'COLON',
] + list(keywords.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_PERCENT = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMI = r';'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'
t_BITNOT = r'~'

t_ignore = ' \t\r'


def t_ARROW(t):
    r'->'
    return t


def t_PLUSPLUS(t):
    r'\+\+'
    return t


def t_MINUSMINUS(t):
    r'--'
    return t


def t_PLUSEQ(t):
    r'\+='
    return t


def t_MINUSEQ(t):
    r'-='
    return t


def t_EQ(t):
    r'=='
    return t


def t_NE(t):
    r'!='
    return t


def t_LE(t):
    r'<='
    return t


def t_GE(t):
    r'>='
    return t


def t_SHL(t):
    r'<<'
    return t


def t_SHR(t):
    r'>>'
    return t


def t_AND(t):
    r'&&'
    return t


def t_OR(t):
    r'\|\|'
    return t


def t_LT(t):
    r'<'
    return t


def t_GT(t):
    r'>'
    return t


def t_NOT(t):
    r'!'
    return t


def t_BITAND(t):
    r'&'
    return t


def t_BITOR(t):
    r'\|'
    return t


def t_BITXOR(t):
    r'\^'
    return t


def t_ASSIGN(t):
    r'='
    return t


def t_NUMBER(t):
    r'0[xX][0-9a-fA-F]+|\d+'
    if t.value.lower().startswith('0x'):
        t.value = int(t.value, 16)
    else:
        t.value = int(t.value)
    return t


def t_CHARLIT(t):
    r"'(\\.|[^\\'])'"
    body = t.value[1:-1]
    if body.startswith('\\'):
        esc = {'n': 10, 't': 9, '0': 0, '\\': 92, "'": 39, 'r': 13}
        t.value = esc.get(body[1], ord(body[1]))
    else:
        t.value = ord(body)
    return t


def t_STRINGLIT(t):
    r'"(\\.|[^\\"])*"'
    raw = t.value[1:-1]
    out = []
    i = 0
    while i < len(raw):
        c = raw[i]
        if c == '\\' and i + 1 < len(raw):
            nc = raw[i + 1]
            out.append({'n': '\n', 't': '\t', '0': '\0', '\\': '\\', '"': '"'}.get(nc, nc))
            i += 2
        else:
            out.append(c)
            i += 1
    t.value = ''.join(out)
    return t


def t_IDENT(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = keywords.get(t.value, 'IDENT')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT_LINE(t):
    r'//[^\n]*'
    pass


def t_COMMENT_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass


def t_error(t):
    raise SyntaxError(f"字句解析エラー: 不正な文字 {t.value[0]!r} (行 {t.lineno})")


def build_lexer():
    return lex.lex()
