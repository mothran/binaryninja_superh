import struct

from binaryninja import (
    InstructionTextToken,
    InstructionTextTokenType
)

from .opcodes import OPCODES, OpType, Oper


class SHInsn:
    def __init__(self, opcode, raw_insn, addr):
        self.opcode = opcode
        self.args = dict()
        self.insn_str = ""
        self.tokens = list()
        self.size = opcode["size"]
        self.raw_insn = raw_insn
        self.addr = addr

    def parse_it(self):
        self._parse_args()
        return self._stringify()

    def _stringify(self):
        for token in self.opcode["tokens"]:
            (toke_type, fmt) = token

            text = fmt.format(
                n=self.args['n'],
                m=self.args['m'],
                imm=self.args['imm'],
                disp=self.args['disp']
            )

            self.tokens.append((toke_type, text))
            self.insn_str += text

        for operand in self.opcode["args"]:
            if operand.type == OpType.REG:
                operand.reg = operand.fmt_str.format(n=self.args['n'], m=self.args['m'])
            elif operand.type == OpType.IMM:
                operand.val = self.args['imm']
            elif operand.type == OpType.DISP:
                operand.val = self.args['disp']

        return True

    def _parse_args(self):
        """Given an instruction and an opcode, return a dict representing them"""
        if self.opcode['m'][0] != 0:
            self.args['m'] = (self.raw_insn & self.opcode['m'][0]) >> self.opcode['m'][1]
        else:
            self.args['m'] = None
        if self.opcode['n'][0] != 0:
            self.args['n'] = (self.raw_insn & self.opcode['n'][0]) >> self.opcode['n'][1]
        else:
            self.args['n'] = None
        if self.opcode['imm'][0] != 0:
            self.args['imm'] = (self.raw_insn & self.opcode['imm'][0]) >> self.opcode['imm'][1]
        else:
            self.args['imm'] = None
        if self.opcode['disp'] != 0:
            if self.opcode["is_label"]:
                self.args['disp'] = self.raw_insn & self.opcode['disp']
                self.args['disp'] = (self.args['disp'] * 2) + self.addr  + 4
            else:
                self.args['disp'] = self.raw_insn & self.opcode['disp']

        else:
            self.args['disp'] = None

def _disasm_sized(raw_insn, addr, size):
    fmt = "<H"
    if size == 4:
        fmt = "<I"

    insn_int = struct.unpack(fmt, raw_insn[:size])[0]

    for opcode in OPCODES:
        if opcode["size"] != size:
            continue

        instbits, instmask = opcode['opmask']
        if insn_int & instmask == instbits:
            insn_obj = SHInsn(opcode, insn_int, addr)
            if not insn_obj.parse_it():
                return None
            return insn_obj

    return None

def disasm_single(raw_insn, addr):
    buf_len = len(raw_insn)
    # if buf_len > 2:
    #     ret = _disasm_sized(raw_insn, addr, 4)
    #     if ret is not None:
    #         return ret

    if buf_len > 0:
        ret = _disasm_sized(raw_insn, addr, 2)
        if ret is not None:
            return ret

    return None