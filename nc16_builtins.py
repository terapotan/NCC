# -*- coding: utf-8 -*-
"""
NC16C 組み込み関数（MomoOSシステムコールのラッパー）のシグネチャ定義。
実際のレジスタ割り当て・syscall発行コードは codegen.py 側で個別に実装する
（out引数のポインタ経由での書き戻しなど、レジスタ規約が個々に異なるため）。
"""
from symtab import UINT, CHAR, PointerType


class BuiltinSig:
    def __init__(self, name, ret_type, params, syscall_num, doc):
        self.name = name
        self.ret_type = ret_type
        self.params = params  # list of (name, Type)  型チェック用
        self.syscall_num = syscall_num
        self.doc = doc


CHARP = PointerType(CHAR)
UINTP = PointerType(UINT)

BUILTIN_SIGNATURES = {
    'input_user_string': BuiltinSig(
        'input_user_string', UINT, [('buf', CHARP)], 0,
        "戻り値：0=成功、1=権限エラー"),
    'compare_to_string': BuiltinSig(
        'compare_to_string', UINT, [('s1', CHARP), ('s2', CHARP)], 1,
        "戻り値：1=等しい、0=等しくない、2=権限エラー"),
    'read_rom_data': BuiltinSig(
        'read_rom_data', UINT,
        [('rom_io_addr', UINT), ('src_addr', UINT), ('length_words', UINT), ('dest_addr', UINT)], 2,
        "戻り値：0=成功、1=権限エラー"),
    'output_string': BuiltinSig(
        'output_string', UINT, [('str', CHARP)], 3,
        "戻り値：0=成功、1=権限エラー"),
    'ascii_to_int': BuiltinSig(
        'ascii_to_int', UINT, [('str', CHARP), ('out_value', UINTP)], 4,
        "戻り値：0=成功、1=不正な文字、2=空文字列、3=権限エラー。変換結果はout_valueに書き込まれる"),
    'int_to_ascii': BuiltinSig(
        'int_to_ascii', UINT, [('value', UINT), ('buf', CHARP)], 5,
        "戻り値：0=成功、1=権限エラー"),
    'divide': BuiltinSig(
        'divide', UINT,
        [('dividend', UINT), ('divisor', UINT), ('remainder', UINTP), ('status', UINTP)], 6,
        "戻り値：商。余りはremainderに、状態(0=成功,1=ゼロ除算)はstatusに書き込まれる"),
}
