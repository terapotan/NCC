# -*- coding: utf-8 -*-
"""
簡易NC-16エミュレータ（NC16Cコンパイラの出力を検証するためのテストツール）。

【重要な注意】
これは実機やLogisim-evolution上の実装を再現するサイクル精度のシミュレータではない。
あくまで「NC16Cコンパイラが生成したアセンブリのロジック（制御フロー・スタック操作・
算術演算・システムコールとのレジスタ受け渡し）が意図通りかどうか」をこの環境内で
検証するためだけの簡易ツールである。命令のアドレス割り当て方式も実機の8バイト命令
とは異なる単純化を行っている（1命令=1アドレスとして扱う）。
実機での最終確認は別途customasm＋Logisim-evolution等で行うこと。
"""
import re


def u16(x):
    return x & 0xFFFF


class Emulator:
    def __init__(self, text, syscall_handler=None, max_steps=2_000_000):
        self.regs = {r: 0 for r in ['a', 'b', 'c', 'd', 'e', 'bp', 'sp']}
        self.mem = {}
        self.labels = {}
        self.instrs = []
        self.syscall_handler = syscall_handler or self.default_syscall
        self.max_steps = max_steps
        self.output = []
        self._assemble(text)
        self.regs['sp'] = 0xF000  # スタック領域の初期値（適当な高位アドレス）

    # ------------------------------------------------------------
    def _assemble(self, text):
        addr = 0
        pending_label = []
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            raw = lines[i]
            line = raw.split(';', 1)[0].strip()
            i += 1
            if not line:
                continue
            if line.startswith('#include'):
                continue
            if line.startswith('#align'):
                n = int(line.split()[1])
                if addr % n != 0:
                    addr += n - (addr % n)
                continue
            if line.startswith('#res'):
                n = int(line.split()[1])
                for lbl in pending_label:
                    self.labels[lbl] = addr
                pending_label = []
                for _ in range(n):
                    self.mem[addr] = 0
                    addr += 1
                continue
            if line.startswith('#d'):
                for lbl in pending_label:
                    self.labels[lbl] = addr
                pending_label = []
                rest = line[2:].strip()
                if rest.startswith('"'):
                    s = self._parse_string_literal(rest)
                    words = self._pack_string(s)
                    for w in words:
                        self.mem[addr] = w
                        addr += 1
                else:
                    val = int(rest, 0)
                    self.mem[addr] = u16(val)
                    addr += 1
                continue
            m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):$', line)
            if m:
                pending_label.append(m.group(1))
                continue
            # 通常命令
            for lbl in pending_label:
                self.labels[lbl] = addr
            pending_label = []
            self.instrs.append(line)
            addr += 1
        # ラベルの前方参照解決のため、命令列は addr(index) == instrs のインデックスに一致させている

    @staticmethod
    def _parse_string_literal(rest):
        assert rest.startswith('"') and rest.endswith('"')
        raw = rest[1:-1]
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
        return ''.join(out)

    @staticmethod
    def _pack_string(s):
        words = []
        chars = [ord(c) for c in s] + [0]  # NULL終端
        i = 0
        while i < len(chars):
            hi = chars[i]
            lo = chars[i + 1] if i + 1 < len(chars) else 0
            words.append(u16((hi << 8) | lo))
            if hi == 0:
                break
            i += 2
            if lo == 0:
                break
        return words

    # ------------------------------------------------------------
    def read_mem_string(self, addr):
        out = []
        while True:
            w = self.mem.get(addr, 0)
            hi = (w >> 8) & 0xFF
            lo = w & 0xFF
            if hi == 0:
                break
            out.append(chr(hi))
            if lo == 0:
                break
            out.append(chr(lo))
            addr += 1
        return ''.join(out)

    def write_mem_string(self, addr, s):
        chars = [ord(c) for c in s] + [0]
        i = 0
        while i < len(chars):
            hi = chars[i]
            lo = chars[i + 1] if i + 1 < len(chars) else 0
            self.mem[addr] = u16((hi << 8) | lo)
            if hi == 0:
                break
            i += 2
            addr += 1
            if lo == 0:
                break

    # ------------------------------------------------------------
    def default_syscall(self, emu):
        num = emu.regs['e']
        if num == 1:  # compare_to_string
            s1 = emu.read_mem_string(emu.regs['a'])
            s2 = emu.read_mem_string(emu.regs['b'])
            emu.regs['c'] = 1 if s1 == s2 else 0
        elif num == 3:  # output_string
            s = emu.read_mem_string(emu.regs['b'])
            emu.output.append(s)
            emu.regs['c'] = 0
        elif num == 4:  # ascii_to_int
            s = emu.read_mem_string(emu.regs['a'])
            if s == '' :
                emu.regs['c'] = 2
            elif not all(ch.isdigit() for ch in s):
                emu.regs['c'] = 1
            else:
                emu.regs['b'] = u16(int(s))
                emu.regs['c'] = 0
        elif num == 5:  # int_to_ascii
            v = emu.regs['a']
            emu.write_mem_string(emu.regs['b'], str(v))
            emu.regs['c'] = 0
        elif num == 6:  # divide
            a, b = emu.regs['a'], emu.regs['b']
            if b == 0:
                emu.regs['c'] = 0
                emu.regs['d'] = 0
                emu.regs['e'] = 1
            else:
                emu.regs['c'] = a // b
                emu.regs['d'] = a % b
                emu.regs['e'] = 0
        else:
            emu.regs['b'] = 0
            emu.regs['c'] = 0
            emu.regs['e'] = 0
        emu.regs['bp'] = 0

    # ------------------------------------------------------------
    def _val(self, tok):
        tok = tok.strip()
        if tok in self.regs:
            return self.regs[tok]
        if tok in self.labels:
            return self.labels[tok]
        if tok.startswith('0x') or tok.startswith('0X'):
            return u16(int(tok, 16))
        return u16(int(tok))

    def run(self, entry_label='program_start'):
        pc = self.labels[entry_label]
        steps = 0
        while True:
            steps += 1
            if steps > self.max_steps:
                raise RuntimeError("最大ステップ数を超えました（無限ループの可能性）")
            if pc >= len(self.instrs):
                break
            line = self.instrs[pc]
            npc = pc + 1
            npc = self._exec(line, pc, npc)
            if npc is None:
                break
            pc = npc

    def _exec(self, line, pc, npc):
        m = re.match(r'^(\w+)\s*(.*)$', line)
        op = m.group(1)
        rest = m.group(2)
        args = [a.strip() for a in rest.split(',')] if rest else []

        R = self.regs

        if op == 'mov':
            dst, src = args
            if dst == 'memaddr':
                R['__memaddr'] = self._val(src)
            elif dst == 'memval':
                R['__memval'] = self._val(src)
            elif dst.startswith('[memaddr'):
                addr = R['__memaddr']
                self.mem[addr] = u16(R['__memval'])
            elif src.startswith('[memaddr'):
                addr = R['__memaddr']
                R[dst] = self.mem.get(addr, 0)
            elif src == 'memval':
                R[dst] = u16(R.get('__memval', 0))
            elif src == 'memaddr':
                R[dst] = u16(R.get('__memaddr', 0))
            else:
                R[dst] = self._val(src)
        elif op in ('add', 'sub', 'mul', 'and_', 'and', 'or', 'xor'):
            dst, src = args
            v = self._val(src)
            if op == 'add':
                R[dst] = u16(R[dst] + v)
            elif op == 'sub':
                R[dst] = u16(R[dst] - v)
            elif op == 'mul':
                R[dst] = u16(R[dst] * v)
            elif op == 'and':
                R[dst] = u16(R[dst] & v)
            elif op == 'or':
                R[dst] = u16(R[dst] | v)
            elif op == 'xor':
                R[dst] = u16(R[dst] ^ v)
        elif op == 'not':
            dst = args[0]
            R[dst] = u16(~R[dst])
        elif op == 'shr':
            dst, src = args
            R[dst] = u16(R[dst] >> self._val(src))
        elif op == 'cmp':
            a, b = args
            R['__cmp'] = (self._val(a), self._val(b))
        elif op in ('je', 'jne', 'jl', 'jle', 'ja', 'jae', 'jz', 'jnz'):
            k, l = R['__cmp']
            take = {
                'je': k == l, 'jne': k != l,
                'jl': u16(k - l) >= 0x8000,
                'jle': (k == l) or (u16(k - l) >= 0x8000),
                'ja': (k != l) and not (u16(k - l) >= 0x8000),
                'jae': not (u16(k - l) >= 0x8000),
            }[op]
            if take:
                return self.labels[args[0]]
            return npc
        elif op == 'jmp':
            return self.labels[args[0]]
        elif op == 'push':
            R['sp'] = u16(R['sp'] - 1)
            self.mem[R['sp']] = self._val(args[0])
        elif op == 'pop':
            v = self.mem.get(R['sp'], 0)
            R['sp'] = u16(R['sp'] + 1)
            R[args[0]] = v
        elif op == 'call':
            R['sp'] = u16(R['sp'] - 1)
            self.mem[R['sp']] = npc
            return self.labels[args[0]]
        elif op == 'ret':
            v = self.mem.get(R['sp'], 0)
            R['sp'] = u16(R['sp'] + 1)
            return v
        elif op == 'syscall':
            self.syscall_handler(self)
        elif op == 'userret':
            return None
        elif op == 'hlt':
            return None
        elif op == 'nop':
            pass
        else:
            raise RuntimeError(f"未対応の命令です（エミュレータ側の制約）: {line}")
        return npc
