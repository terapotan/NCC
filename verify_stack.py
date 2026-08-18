# -*- coding: utf-8 -*-
"""
生成されたアセンブリの各関数について、push/popの深さがどの経路を通っても
一致するかを検証する簡易ベリファイア（バグ発見用）。
"""
import re
import sys


def analyze(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    # 関数ごとに分割: 「名前:」で始まり、次の「名前:」(関数と分かるもの)まで
    # 単純化のため、"push bp" の直後に "mov bp,sp" がある行を関数開始とみなす
    func_starts = []
    for i, l in enumerate(lines):
        s = l.strip()
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):$', s)
        if m and i + 1 < len(lines) and lines[i + 1].strip() == 'push bp':
            func_starts.append((i, m.group(1)))
    func_starts.append((len(lines), None))

    problems = []
    for idx in range(len(func_starts) - 1):
        start, name = func_starts[idx]
        end, _ = func_starts[idx + 1]
        seg = lines[start:end]
        problems.extend(verify_func(name, seg))
    return problems


def verify_func(name, seg):
    # ラベル -> セグメント内インデックス
    label_idx = {}
    instrs = []
    for l in seg:
        s = l.split(';', 1)[0].strip()
        if not s:
            continue
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):$', s)
        if m:
            label_idx[m.group(1)] = len(instrs)
        else:
            instrs.append(s)

    depth_at = {}
    problems = []
    # BFS/DFS
    stack = [(0, 0)]
    visited_edges = set()
    while stack:
        i, d = stack.pop()
        if i >= len(instrs):
            continue
        if i in depth_at:
            if depth_at[i] != d:
                problems.append(
                    f"[{name}] 命令{i} '{instrs[i]}' に経路によって異なる深さで到達"
                    f"（{depth_at[i]} vs {d}）")
            continue
        depth_at[i] = d
        line = instrs[i]
        nd = d
        if line.startswith('push '):
            nd = d + 1
        elif line.startswith('pop '):
            nd = d - 1
        elif line.startswith('sub sp,'):
            nd = d + int(line.split(',')[1])
        elif line.startswith('add sp,'):
            nd = d - int(line.split(',')[1])
        elif line.startswith('mov sp,bp'):
            nd = 0  # フレームポインタでリセット（局所変数領域の外側=呼び出し規約上の基準に戻る）

        m = re.match(r'^(jmp|je|jne|jl|jle|ja|jae)\s+(\S+)$', line)
        if m:
            target = label_idx.get(m.group(2))
            if target is not None:
                stack.append((target, nd))
            if m.group(1) != 'jmp':
                stack.append((i + 1, nd))
            continue
        if line == 'ret':
            if d != 0:
                problems.append(f"[{name}] retの直前でスタック深さが0ではありません（深さ={d}） 命令{i}: 直前一部={instrs[max(0,i-3):i]}")
            continue
        stack.append((i + 1, nd))
    return problems


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'examples/example1.asm'
    problems = analyze(path)
    if not problems:
        print("問題は見つかりませんでした。")
    else:
        for p in problems:
            print(p)
