from enum import Enum
from binaryninja import InstructionTextToken, InstructionTextTokenType



class OpType(Enum):
    REG=1
    IMM=2
    DISP=3
    UNKNOWN=5

class Oper:
    def __init__(self, otype, fmt_str, is_ref, is_pair, mod_reg, size):
        self.type = otype
        self.fmt_str = fmt_str
        self.is_ref = is_ref
        self.is_pair = is_pair
        self.mod_reg = mod_reg
        self.size = size


OPCODES = (
    {
        'opmask': (0x6003, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xe000, 0xf000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'mov',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00000000, 0xf00f0000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0xf0, 0x4),
        'disp': 0x0,
        'cmd': 'movi20',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 3),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movi20'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00010000, 0xf00f0000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0xf0, 0x4),
        'disp': 0x0,
        'cmd': 'movi20s',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 3),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movi20s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xc700, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mova',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'PC', False, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mova'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'PC'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x9000, 0xf000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'PC', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'PC'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xd000, 0xf000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'PC', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'PC'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x6000, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x6001, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x6002, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2000, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2001, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2002, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x6004, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 1, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x6005, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 2, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x6006, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2004, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -1, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2005, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -2, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2006, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x40cb, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, -1, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x40db, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, -2, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x40eb, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, -4, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x408b, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 1, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0x409b, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 2, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0x40ab, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0x8400, 0xff00),
        'm': (0xf0, 0x4),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xf,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x30014000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x30018000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movu.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movu.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x8500, 0xff00),
        'm': (0xf0, 0x4),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xf,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x30015000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x30019000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movu.w',
        'width': 2,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movu.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x5000, 0xf000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0xf,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x30016000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x8000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0xf0, 0x4),
        'imm': (0x0, 0x0),
        'disp': 0xf,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x30010000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x8100, 0xff00),
        'm': (0x0, 0x0),
        'n': (0xf0, 0x4),
        'imm': (0x0, 0x0),
        'disp': 0xf,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x30011000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x1000, 0xf000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0xf,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x30012000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x000c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x000d, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x000e, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0004, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x0005, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x0006, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0xc400, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'GBR', False, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0xc500, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'GBR', False, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0xc600, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'GBR', False, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0xc000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mov.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0xc100, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mov.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0xc200, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'mov.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mov.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x0073, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movco.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movco.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0063, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movli.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movli.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x40a9, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movua.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movua.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x40e9, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movua.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movua.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x40f1, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movml.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R15', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movml.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R15')
        ],
    },
    {
        'opmask': (0x40f5, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movml.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R15', True, False, 4, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movml.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R15'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x40f0, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movmu.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R15', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movmu.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R15')
        ],
    },
    {
        'opmask': (0x40f4, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movmu.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R15', True, False, 4, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movmu.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R15'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0039, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movrt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movrt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0029, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0068, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'nott',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'nott'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x6008, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'swap.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'swap.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x6009, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'swap.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'swap.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x200d, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'xtrct',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'xtrct'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x30094000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'band.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, False, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'band.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x3009c000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bandnot.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bandnot.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x30090000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bclr.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bclr.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x8600, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0xf0, 0x4),
        'imm': (0x7, 0x0),
        'disp': 0x0,
        'cmd': 'bclr',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bclr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x30093000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bld.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bld.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x8708, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0xf0, 0x4),
        'imm': (0x7, 0x0),
        'disp': 0x0,
        'cmd': 'bld',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bld'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x3009b000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bldnot.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bldnot.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x30095000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bor.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bor.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x3009d000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bornot.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bornot.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x30091000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bset.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bset.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x8608, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0xf0, 0x4),
        'imm': (0x7, 0x0),
        'disp': 0x0,
        'cmd': 'bset',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bset'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x30092000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bst.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bst.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x8700, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0xf0, 0x4),
        'imm': (0x7, 0x0),
        'disp': 0x0,
        'cmd': 'bst',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bst'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x30096000, 0xf0fff000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bxor.b',
        'width': 1,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bxor.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x300c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'add',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'add'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x7000, 0xf000),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'add',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'add'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x300e, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'addc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'addc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x300f, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'addv',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'addv'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x8800, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/eq',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/eq'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x3000, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/eq',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/eq'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x3002, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/hs',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/hs'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x3003, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/ge',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/ge'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x3006, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/hi',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/hi'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x3007, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/gt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/gt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4015, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/pl',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/pl'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4011, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/pz',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/pz'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x200c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'cmp/str',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'cmp/str'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4091, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'clips.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'clips.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4095, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'clips.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'clips.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4081, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'clipu.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'clipu.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4085, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'clipu.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'clipu.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2007, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'div0s',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'div0s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0019, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'div0u',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'div0u'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x3004, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'div1',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'div1'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4094, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'divs',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'divs'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4084, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'divu',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'divu'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x300d, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dmuls.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dmuls.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x3005, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dmulu.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dmulu.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4010, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x600e, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'exts.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'exts.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x600f, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'exts.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'exts.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x600c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'extu.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'extu.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x600d, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'extu.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'extu.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x000f, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mac.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'R{n}', True, False, 4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mac.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0x400f, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mac.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 2, 0),
            Oper(OpType.REG, 'R{n}', True, False, 2, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mac.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0x0007, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mul.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mul.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4080, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mulr',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mulr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x200f, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'muls.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'muls.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x200e, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'mulu.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'mulu.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x600b, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'neg',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'neg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x600a, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'negc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'negc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x3008, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sub',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sub'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x300a, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'subc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'subc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x300b, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'subv',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'subv'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2009, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'and',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'and'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xc900, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'and',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'and'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0xcd00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'and.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'and.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x6007, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'not',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'not'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x200b, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'or',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'or'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xcb00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'or',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'or'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0xcf00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'or.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'or.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x401b, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'tas.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'tas.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x2008, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'tst',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'tst'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xc800, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'tst',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'tst'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0xcc00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'tst.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'tst.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x200a, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'xor',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'xor'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xca00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'xor',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'xor'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0xce00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'xor.b',
        'width': 1,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'xor.b'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x4024, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'rotcl',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'rotcl'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4025, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'rotcr',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'rotcr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4004, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'rotl',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'rotl'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4005, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'rotr',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'rotr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x400c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shad',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shad'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4020, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shal',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shal'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4021, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shar',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shar'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x400d, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shld',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shld'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4000, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shll',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shll'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4008, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shll2',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shll2'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4018, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shll8',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shll8'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4028, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shll16',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shll16'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4001, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shlr',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shlr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4009, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shlr2',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shlr2'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4019, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shlr8',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shlr8'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4029, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'shlr16',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'shlr16'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x8b00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'bf',
        'width': 0,
        'size': 2,
        'is_label': True,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', False, False, 0, 2)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bf'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}')
        ],
    },
    {
        'opmask': (0x8f00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'bf/s',
        'width': 0,
        'size': 2,
        'is_label': True,
        'is_delay': True,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', False, False, 0, 2)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bf/s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}')
        ],
    },
    {
        'opmask': (0x8900, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'bt',
        'width': 0,
        'size': 2,
        'is_label': True,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', False, False, 0, 2)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}')
        ],
    },
    {
        'opmask': (0x8d00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'bt/s',
        'width': 0,
        'size': 2,
        'is_label': True,
        'is_delay': True,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', False, False, 0, 2)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bt/s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}')
        ],
    },
    {
        'opmask': (0xa000, 0xf000),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xfff,
        'cmd': 'bra',
        'width': 0,
        'size': 2,
        'is_label': True,
        'is_delay': True,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', False, False, 0, 2)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bra'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}')
        ],
    },
    {
        'opmask': (0x0023, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'braf',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': True,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'braf'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}')
        ],
    },
    {
        'opmask': (0xb000, 0xf000),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xfff,
        'cmd': 'bsr',
        'width': 0,
        'size': 2,
        'is_label': True,
        'is_delay': True,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', False, False, 0, 2)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bsr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}')
        ],
    },
    {
        'opmask': (0x0003, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'bsrf',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': True,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'bsrf'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}')
        ],
    },
    {
        'opmask': (0x402b, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'jmp',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': True,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'jmp'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}')
        ],
    },
    {
        'opmask': (0x400b, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'jsr',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': True,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'jsr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}')
        ],
    },
    {
        'opmask': (0x404b, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'jsr/n',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'jsr/n'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}')
        ],
    },
    {
        'opmask': (0x8300, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'jsr/n',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'TBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'jsr/n'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'TBR'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x000b, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'rts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': True,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'rts'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x006b, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'rts/n',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'rts/n'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x007b, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'rtv/n',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'rtv/n'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}')
        ],
    },
    {
        'opmask': (0x0028, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'clrmac',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'clrmac'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x0048, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'clrs',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'clrs'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x0008, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'clrt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'clrt'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x00e3, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'icbi',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'icbi'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x40e5, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldbank',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.REG, 'R0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldbank'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R0')
        ],
    },
    {
        'opmask': (0x400e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'SR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'SR')
        ],
    },
    {
        'opmask': (0x4007, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'SR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'SR')
        ],
    },
    {
        'opmask': (0x404a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'TBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'TBR')
        ],
    },
    {
        'opmask': (0x401e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR')
        ],
    },
    {
        'opmask': (0x4017, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'GBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'GBR')
        ],
    },
    {
        'opmask': (0x402e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'VBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'VBR')
        ],
    },
    {
        'opmask': (0x4027, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'VBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'VBR')
        ],
    },
    {
        'opmask': (0x405e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'MOD', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MOD')
        ],
    },
    {
        'opmask': (0x4057, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'MOD', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MOD')
        ],
    },
    {
        'opmask': (0x407e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'RE', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'RE')
        ],
    },
    {
        'opmask': (0x4077, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'RE', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'RE')
        ],
    },
    {
        'opmask': (0x406e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'RS', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'RS')
        ],
    },
    {
        'opmask': (0x4067, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'RS', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'RS')
        ],
    },
    {
        'opmask': (0x403a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'SGR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'SGR')
        ],
    },
    {
        'opmask': (0x4036, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'SGR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'SGR')
        ],
    },
    {
        'opmask': (0x403e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'SSR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'SSR')
        ],
    },
    {
        'opmask': (0x4037, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'SSR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'SSR')
        ],
    },
    {
        'opmask': (0x404e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'SPC', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'SPC')
        ],
    },
    {
        'opmask': (0x4047, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'SPC', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'SPC')
        ],
    },
    {
        'opmask': (0x40fa, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'DBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'DBR')
        ],
    },
    {
        'opmask': (0x40f6, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'DBR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'DBR')
        ],
    },
    {
        'opmask': (0x408e, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}_BANK', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}_BANK')
        ],
    },
    {
        'opmask': (0x4087, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'R{n}_BANK', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}_BANK')
        ],
    },
    {
        'opmask': (0x8e00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'ldre',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'PC', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldre'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'PC'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x8c00, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0xff,
        'cmd': 'ldrs',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 1),
            Oper(OpType.REG, 'PC', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldrs'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'PC'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x400a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'MACH', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACH')
        ],
    },
    {
        'opmask': (0x4006, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'MACH', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACH')
        ],
    },
    {
        'opmask': (0x401a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'MACL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACL')
        ],
    },
    {
        'opmask': (0x4016, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'MACL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACL')
        ],
    },
    {
        'opmask': (0x402a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'PR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'PR')
        ],
    },
    {
        'opmask': (0x4026, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'PR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'PR')
        ],
    },
    {
        'opmask': (0x406a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'DSR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'DSR')
        ],
    },
    {
        'opmask': (0x4066, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'DSR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'DSR')
        ],
    },
    {
        'opmask': (0x4076, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'A0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'A0')
        ],
    },
    {
        'opmask': (0x4076, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'A0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'A0')
        ],
    },
    {
        'opmask': (0x408a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'X0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'X0')
        ],
    },
    {
        'opmask': (0x4086, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'X0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'X0')
        ],
    },
    {
        'opmask': (0x409a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'X1', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'X1')
        ],
    },
    {
        'opmask': (0x4096, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'X1', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'X1')
        ],
    },
    {
        'opmask': (0x40aa, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'Y0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'Y0')
        ],
    },
    {
        'opmask': (0x40a6, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'Y0', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'Y0')
        ],
    },
    {
        'opmask': (0x40ba, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'Y1', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'Y1')
        ],
    },
    {
        'opmask': (0x40b6, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'Y1', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'Y1')
        ],
    },
    {
        'opmask': (0x0038, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ldtlb',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ldtlb'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x00c3, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movca.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movca.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0009, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'nop',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'nop'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x0093, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ocbi',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ocbi'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00a3, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ocbp',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ocbp'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00b3, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ocbwb',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ocbwb'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0083, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pref',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pref'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00d3, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'prefi',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'prefi'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x005b, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'resbank',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'resbank'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x002b, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'rte',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': True,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'rte'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x4014, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'setrc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'setrc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x8200, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'setrc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'setrc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}')
        ],
    },
    {
        'opmask': (0x0058, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sets',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sets'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x0018, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sett',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sett'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x001b, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sleep',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sleep'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0x40e1, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stbank',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stbank'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0002, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'SR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'SR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4003, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'SR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'SR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x004a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'TBR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'TBR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0012, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'GBR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4013, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'GBR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'GBR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0022, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'VBR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'VBR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4023, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'VBR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'VBR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0052, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MOD', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MOD'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4053, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MOD', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MOD'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0072, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'RE', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'RE'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4073, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'RE', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'RE'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0062, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'RS', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'RS'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4063, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'RS', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'RS'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x003a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'SGR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'SGR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4032, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'SGR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'SGR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0032, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'SSR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'SSR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4033, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'SSR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'SSR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0042, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'SPC', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'SPC'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4043, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'SPC', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'SPC'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00fa, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'DBR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'DBR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x40f2, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'DBR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'DBR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x0082, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}_BANK', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}_BANK'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4083, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'stc.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}_BANK', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'stc.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}_BANK'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x000a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACH', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACH'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4002, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACH', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACH'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x001a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACL', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4012, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACL', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x002a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'PR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'PR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4022, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'PR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'PR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x006a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'DSR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'DSR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4062, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'DSR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'DSR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x007a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'A0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'A0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4062, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'A0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'A0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x008a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'X0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'X0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4082, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'X0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'X0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x009a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'X1', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'X1'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4092, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'X1', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'X1'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00aa, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'Y0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'Y0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x40a2, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'Y0', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'Y0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00ba, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'Y1', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'Y1'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x40b2, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'Y1', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'Y1'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x00ab, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'synco',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'synco'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0xc300, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0xff, 0x0),
        'disp': 0x0,
        'cmd': 'trapa',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'trapa'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}')
        ],
    },
    {
        'opmask': (0xf00c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf008, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.s',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf00a, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.s',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xf009, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.s',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf00b, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.s',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xf006, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.s',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf007, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.s',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x30017000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.s',
        'width': 4,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0x30013000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.s',
        'width': 4,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.s'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0xf00c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf00c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'XDn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'XDn')
        ],
    },
    {
        'opmask': (0xf00c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'XDm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'XDm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf00c, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'XDm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'XDn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'XDm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'XDn')
        ],
    },
    {
        'opmask': (0xf008, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf008, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'XDn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'XDn')
        ],
    },
    {
        'opmask': (0xf00a, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xf00a, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'XDm', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'XDm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xf009, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 8, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf009, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 8, 0),
            Oper(OpType.UNKNOWN, 'XDn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'XDn')
        ],
    },
    {
        'opmask': (0xf00b, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -8, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xf00b, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'XDm', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -8, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'XDm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xf006, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf006, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'XDn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'XDn')
        ],
    },
    {
        'opmask': (0xf007, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0xf007, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'XDm', False, False, 0, 0),
            Oper(OpType.REG, 'R0', True, True, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'XDm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.RegisterToken, 'R0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0x30017000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, ')'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0x30013000, 0xf00ff000),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmov.d',
        'width': 8,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.DISP, '0x{disp:x}', True, True, 0, 2),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmov.d'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@('),
            (InstructionTextTokenType.PossibleAddressToken, '0x{disp:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}'),
            (InstructionTextTokenType.TextToken, ')')
        ],
    },
    {
        'opmask': (0xf08d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fldi0',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fldi0'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf09d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fldi1',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fldi1'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf01d, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'flds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FPUL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'flds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FPUL')
        ],
    },
    {
        'opmask': (0xf00d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fsts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPUL', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fsts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPUL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf05d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fabs',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fabs'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf04d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fneg',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fneg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf000, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fadd',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fadd'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf001, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fsub',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fsub'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf002, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmul',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmul'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf00e, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmac',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'FR0', False, False, 0, 0),
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmac'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'FR0'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf003, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fdiv',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fdiv'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf06d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fsqrt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fsqrt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf004, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fcmp/eq',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fcmp/eq'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf005, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fcmp/gt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fcmp/gt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf02d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'float',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPUL', False, False, 0, 0),
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'float'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPUL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf03d, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ftrc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FPUL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ftrc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FPUL')
        ],
    },
    {
        'opmask': (0xf0ed, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fipr',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'FVm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'FVn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fipr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'FVm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'FVn')
        ],
    },
    {
        'opmask': (0xf0fd, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ftrv',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'XMTRX', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'FVn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ftrv'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'XMTRX'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'FVn')
        ],
    },
    {
        'opmask': (0xf07d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fsrra',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FR{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fsrra'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FR{n}')
        ],
    },
    {
        'opmask': (0xf0fd, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fsca',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPUL', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fsca'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPUL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf05d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fabs',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fabs'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf04d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fneg',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fneg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf000, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fadd',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fadd'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf001, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fsub',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fsub'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf002, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fmul',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fmul'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf003, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fdiv',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fdiv'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf06d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fsqrt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fsqrt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf004, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fcmp/eq',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fcmp/eq'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf005, 0xf00f),
        'm': (0xf0, 0x4),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fcmp/gt',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fcmp/gt'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf02d, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'float',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPUL', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'float'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPUL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0xf03d, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'ftrc',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.REG, 'FPUL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'ftrc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FPUL')
        ],
    },
    {
        'opmask': (0xf0bd, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fcnvds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'DRm', False, False, 0, 0),
            Oper(OpType.REG, 'FPUL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fcnvds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'DRm'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FPUL')
        ],
    },
    {
        'opmask': (0xf0ad, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fcnvsd',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPUL', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'DRn', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fcnvsd'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPUL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'DRn')
        ],
    },
    {
        'opmask': (0x406a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FPSCR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FPSCR')
        ],
    },
    {
        'opmask': (0x006a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPSCR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPSCR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4066, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'FPSCR', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FPSCR')
        ],
    },
    {
        'opmask': (0x4062, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPSCR', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPSCR'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x405a, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', False, False, 0, 0),
            Oper(OpType.REG, 'FPUL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FPUL')
        ],
    },
    {
        'opmask': (0x005a, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPUL', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPUL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0x4056, 0xf0ff),
        'm': (0xf00, 0x8),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'lds.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'R{m}', True, False, 4, 0),
            Oper(OpType.REG, 'FPUL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'lds.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.RegisterToken, 'R{m}'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'FPUL')
        ],
    },
    {
        'opmask': (0x4052, 0xf0ff),
        'm': (0x0, 0x0),
        'n': (0xf00, 0x8),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'sts.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'FPUL', False, False, 0, 0),
            Oper(OpType.REG, 'R{n}', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'sts.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'FPUL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.RegisterToken, 'R{n}')
        ],
    },
    {
        'opmask': (0xfbfd, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'frchg',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'frchg'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0xf3fd, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fschg',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fschg'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0xf7fd, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'fpchg',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'fpchg'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0xf000, 0xffff),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'nopx',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'nopx'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0xf004, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movx.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ax', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dx', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movx.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ax'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dx')
        ],
    },
    {
        'opmask': (0xf008, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movx.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ax', True, False, 2, 0),
            Oper(OpType.UNKNOWN, 'Dx', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movx.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ax'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dx')
        ],
    },
    {
        'opmask': (0xf00c, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movx.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ax+Ix', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dx', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movx.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ax+Ix'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dx')
        ],
    },
    {
        'opmask': (0xf004, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movx.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Da', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ax', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movx.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Da'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ax')
        ],
    },
    {
        'opmask': (0xf008, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movx.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Da', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ax', True, False, 2, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movx.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Da'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ax'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0xf00c, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movx.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Da', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ax+Ix', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movx.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Da'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ax+Ix')
        ],
    },
    {
        'opmask': (0xf000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'nopy',
        'width': 0,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'nopy'),
            (InstructionTextTokenType.TextToken, ' ')
        ],
    },
    {
        'opmask': (0xf000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movy.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ay', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dy', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movy.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ay'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dy')
        ],
    },
    {
        'opmask': (0xf000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movy.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ay', True, False, 2, 0),
            Oper(OpType.UNKNOWN, 'Dy', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movy.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ay'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dy')
        ],
    },
    {
        'opmask': (0xf000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movy.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ay+Iy', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dy', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movy.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ay+Iy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dy')
        ],
    },
    {
        'opmask': (0xf000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movy.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Da', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ay', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movy.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Da'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ay')
        ],
    },
    {
        'opmask': (0xf000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movy.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Da', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ay', True, False, 2, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movy.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Da'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ay'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0xf000, 0xff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movy.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Da', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ay+Iy', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movy.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Da'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'Ay+Iy')
        ],
    },
    {
        'opmask': (0xf400, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'As', True, False, -2, 0),
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.TextToken, 'As'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Ds')
        ],
    },
    {
        'opmask': (0xf404, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'As', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Ds')
        ],
    },
    {
        'opmask': (0xf408, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'As', True, False, 2, 0),
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Ds')
        ],
    },
    {
        'opmask': (0xf40c, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'As+Ix', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As+Ix'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Ds')
        ],
    },
    {
        'opmask': (0xf401, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'As', True, False, -2, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Ds'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.TextToken, 'As')
        ],
    },
    {
        'opmask': (0xf405, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'As', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Ds'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As')
        ],
    },
    {
        'opmask': (0xf409, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'As', True, False, 2, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Ds'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0xf40d, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.w',
        'width': 2,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'As+Is', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.w'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Ds'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As+Is')
        ],
    },
    {
        'opmask': (0xf402, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'As', True, False, -4, 0),
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.TextToken, 'As'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Ds')
        ],
    },
    {
        'opmask': (0xf406, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'As', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Ds')
        ],
    },
    {
        'opmask': (0xf40a, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'As', True, False, 4, 0),
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As'),
            (InstructionTextTokenType.TextToken, '+'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Ds')
        ],
    },
    {
        'opmask': (0xf40e, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'As+Is', True, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As+Is'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Ds')
        ],
    },
    {
        'opmask': (0xf403, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'As', True, False, -4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Ds'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@-'),
            (InstructionTextTokenType.TextToken, 'As')
        ],
    },
    {
        'opmask': (0xf407, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'As', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Ds'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As')
        ],
    },
    {
        'opmask': (0xf40b, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'As', True, False, 4, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Ds'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As'),
            (InstructionTextTokenType.TextToken, '+')
        ],
    },
    {
        'opmask': (0xf40f, 0xff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'movs.l',
        'width': 4,
        'size': 2,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Ds', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'As+Is', True, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'movs.l'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Ds'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, '@'),
            (InstructionTextTokenType.TextToken, 'As+Is')
        ],
    },
    {
        'opmask': (0xf8008800, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pabs',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pabs'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a800, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pabs',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pabs'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b100, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'padd',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'padd'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b200, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct padd',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct padd'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b300, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf padd',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf padd'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b000, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'paddc',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'paddc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008d00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pclr',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pclr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008e00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pclr',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pclr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008f00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pclr',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pclr'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008400, 0xff00ff0f),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pcmp',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pcmp'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy')
        ],
    },
    {
        'opmask': (0xf800d900, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pcopy',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pcopy'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800f900, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pcopy',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pcopy'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800da00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pcopy',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pcopy'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800fa00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pcopy',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pcopy'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800db00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pcopy',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pcopy'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800fb00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pcopy',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pcopy'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800c900, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pneg',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pneg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800e900, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pneg',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pneg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800ca00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pneg',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pneg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800ea00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pneg',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pneg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800cb00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pneg',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pneg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800eb00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pneg',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pneg'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a100, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'psub',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'psub'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a200, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct psub',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct psub'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a300, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf psub',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf psub'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a000, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'psubc',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'psubc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008900, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pdec',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pdec'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a900, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pdec',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pdec'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008a00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pdec',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pdec'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800aa00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pdec',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pdec'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008b00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pdec',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pdec'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800ab00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pdec',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pdec'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009900, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pinc',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pinc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b900, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pinc',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pinc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009a00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pinc',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pinc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800ba00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pinc',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pinc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009b00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pinc',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pinc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800bb00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pinc',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pinc'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009d00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pdmsb',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pdmsb'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800bd00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pdmsb',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pdmsb'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009e00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pdmsb',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pdmsb'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800be00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pdmsb',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pdmsb'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009f00, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pdmsb',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pdmsb'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800bf00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pdmsb',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pdmsb'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009800, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'prnd',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'prnd'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b800, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'prnd',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'prnd'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009500, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pand',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pand'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009600, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pand',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pand'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009700, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pand',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pand'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b500, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'por',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'por'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b600, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct por',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct por'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800b700, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf por',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf por'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a500, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pxor',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pxor'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a600, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pxor',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pxor'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800a700, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pxor',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pxor'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8004000, 0xff00f0f0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pmuls',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Se', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sf', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dg', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pmuls'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Se'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sf'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dg')
        ],
    },
    {
        'opmask': (0xf8009100, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'psha',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'psha'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009200, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct psha',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct psha'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8009300, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf psha',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf psha'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8000000, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'psha',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'psha'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008100, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pshl',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pshl'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008200, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct pshl',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct pshl'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8008300, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf pshl',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Sx', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Sy', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf pshl'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Sx'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Sy'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf8001000, 0xff00ff00),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'pshl',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.IMM, '0x{imm:x}', False, False, 0, 1),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'pshl'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.IntegerToken, '0x{imm:x}'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800ed00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'plds',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0),
            Oper(OpType.REG, 'MACH', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'plds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACH')
        ],
    },
    {
        'opmask': (0xf800fd00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'plds',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0),
            Oper(OpType.REG, 'MACL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'plds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACL')
        ],
    },
    {
        'opmask': (0xf800ee00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct plds',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0),
            Oper(OpType.REG, 'MACH', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct plds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACH')
        ],
    },
    {
        'opmask': (0xf800fe00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct plds',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0),
            Oper(OpType.REG, 'MACL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct plds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACL')
        ],
    },
    {
        'opmask': (0xf800ef00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf plds',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0),
            Oper(OpType.REG, 'MACH', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf plds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACH')
        ],
    },
    {
        'opmask': (0xf800ff00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf plds',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0),
            Oper(OpType.REG, 'MACL', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf plds'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.TextToken, 'Dz'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.RegisterToken, 'MACL')
        ],
    },
    {
        'opmask': (0xf800cd00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'psts',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACH', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'psts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACH'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800dd00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'psts',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACL', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'psts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800ce00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct psts',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACH', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct psts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACH'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800de00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dct psts',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACL', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dct psts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800cf00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf psts',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACH', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf psts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACH'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
    {
        'opmask': (0xf800df00, 0xff00fff0),
        'm': (0x0, 0x0),
        'n': (0x0, 0x0),
        'imm': (0x0, 0x0),
        'disp': 0x0,
        'cmd': 'dcf psts',
        'width': 0,
        'size': 4,
        'is_label': False,
        'is_delay': False,
        'args': [
            Oper(OpType.REG, 'MACL', False, False, 0, 0),
            Oper(OpType.UNKNOWN, 'Dz', False, False, 0, 0)
        ],
        'tokens': [
            (InstructionTextTokenType.InstructionToken, 'dcf psts'),
            (InstructionTextTokenType.TextToken, ' '),
            (InstructionTextTokenType.RegisterToken, 'MACL'),
            (InstructionTextTokenType.OperandSeparatorToken, ', '),
            (InstructionTextTokenType.TextToken, 'Dz')
        ],
    },
)
