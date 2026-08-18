# nc16cc — NC16C コンパイラ

NC-16（CPUNC16）アーキテクチャ向けの簡易C風言語「NC16C」を、NC-16アセンブリへ
コンパイルするPython製コンパイラです。

## 必要なもの

- Python 3.8以降
- [ply](https://pypi.org/project/ply/)（`pip install ply`）

## ファイル構成

```
nc16cc/
├── lexer.py         字句解析器 (ply.lex)
├── parser.py         構文解析器 (ply.yacc) → AST
├── ast_nodes.py       ASTノード定義
├── symtab.py          型システム・シンボルテーブル
├── nc16_builtins.py   組み込みsyscallラッパーのシグネチャ定義
├── codegen.py         コード生成器 (AST → NC-16アセンブリ)
├── compiler.py        CLIエントリポイント
├── nc16emu.py         【テスト用】簡易NC-16エミュレータ
├── verify_stack.py    【テスト用】スタック収支の静的検証ツール
├── GRAMMAR.md          言語仕様書（文法・型システム・Cとの相違点など）
├── examples/           サンプルプログラム
└── tests/              機能ごとの単体テストプログラム
```

## 使い方

```bash
pip install ply
python3 compiler.py examples/example1.c16 -o examples/example1.asm
```

生成された `.asm` ファイルは、MomoOSのユーザープログラムとしてそのまま
customasmでアセンブルできる形式です（`#include "nc16_assemble_USERPROGRAM.asm"`
から始まり、`program_start` → `main()` 呼び出し → `userret` という構成）。

言語仕様の詳細（サポートする文法、C言語との相違点、メモリモデル、呼び出し規約、
組み込みsyscall関数の一覧など）は [GRAMMAR.md](./GRAMMAR.md) を参照してください。

## テスト

`tests/` 以下に、配列・構造体・ポインタ・switch・再帰・ビット演算・除算・
組み込みsyscallなど機能ごとの単体テストプログラムと、それを簡易エミュレータ上で
実行して期待値と照合するテストが含まれています。

```bash
python3 compiler.py tests/t_array.c16 -o tests/t_array.asm
python3 verify_stack.py tests/t_array.asm
```

## 開発時に見つかった主なバグと修正（記録）

開発中、以下の重大なバグを簡易エミュレータでの実行検証により発見し、修正しました。

1. **syscall命令によるbpレジスタの破壊**：NC-16の`syscall`命令は仕様上bpレジスタを
   上書きする（成功時0、不正な番号なら1）。本コンパイラはbpをフレームポインタとして
   使うため、syscallを発行する全箇所でbpをpush/popして保護するよう修正。
2. **配列・構造体ローカル変数のサイズ未考慮**：スタックフレーム上のローカル変数に
   常に1ワードしか割り当てていなかったため、複数ワードを要する配列/構造体が
   後続の変数と重なって（エイリアスして）壊れていた。実際の型サイズ分を確保する
   よう修正。
3. **関数引数のpush順序の誤り**：引数を左から右へpushしていたため、呼び出し先から
   見て`bp+2`が第1引数ではなく最後の引数になってしまっていた。右から左へpushする
   よう修正。
