#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NC16C コンパイラ CLI
使い方: python3 compiler.py 入力ファイル.c16 [-o 出力ファイル.asm]
"""
import sys
import argparse
from parser import parse
from codegen import generate
from symtab import CompileError


def main():
    ap = argparse.ArgumentParser(description="NC16C -> NC-16 アセンブリ コンパイラ")
    ap.add_argument('input', help="入力ソースファイル (.c16)")
    ap.add_argument('-o', '--output', help="出力アセンブリファイル (省略時は標準出力)")
    args = ap.parse_args()

    with open(args.input, encoding='utf-8') as f:
        src = f.read()

    try:
        ast = parse(src)
        asm = generate(ast)
    except SyntaxError as e:
        print(f"構文エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except CompileError as e:
        print(f"コンパイルエラー: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(asm)
        print(f"アセンブリを出力しました: {args.output}")
    else:
        print(asm)


if __name__ == '__main__':
    main()
