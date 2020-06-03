import os
import sys

from lxml import html
import requests


def fetch():
    page = requests.get('http://www.shared-ptr.com/sh_insns.html')
    tree = html.fromstring(page.content)

    data = list()

    for row in tree.xpath("//div[@class='col_cont']"):
        insn_class = row.xpath("./div[@class='col_cont_1']/text()")[0]
        insn_text = row.xpath("./div[@class='col_cont_2']/text()")[0]
        desc_text = row.xpath("./div[@class='col_cont_3']/text()")[0]
        is_delay = False
        if "Delayed branch" in desc_text:
            is_delay = True

        bit_pat = row.xpath("./div[@class='col_cont_4']/text()")[0]
        bit_pat = bit_pat.replace(" ", "")
        insn_text = insn_text.replace("\t\t", " ").replace("\t", " ")

        # TODO: resolve duplex instructions
        #  eg: padd-pmuls and psub-pmuls
        if "\n" in insn_text:
            continue

        insn_text = ' '.join(insn_text.split())
        data.append( (insn_text, bit_pat, is_delay) )

    return data

oper_str = """
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

"""

replace_regs = [
    "R0",
    "R15",
    "GBR",
    "TBR",
    "SR",
    "VBR",
    "MOD",
    "RE",
    "RS",
    "SGR",
    "SSR",
    "SPC",
    "DBR",
    "MACH",
    "MACL",
    "PR",
    "DSR",
    "A0",
    "X0",
    "X1",
    "Y0",
    "Y1",
    "PC",
    "FPSCR",
    "FPUL",
]

def parse(data):
    output = list()
    output.append("from enum import Enum")
    output.append("from binaryninja import InstructionTextToken, InstructionTextTokenType\n\n")
    output.append(oper_str)
    output.append("OPCODES = (")

    for elm in data:
        (insn_text, bit_pat, is_delay) = elm

        tokens = list()
        if insn_text.startswith("dcf") or insn_text.startswith("dct"):
            cmd = ' '.join(insn_text.split(" ")[0:2])
        else:
            cmd = insn_text.split(" ")[0]

        tokens.append(f"(InstructionTextTokenType.InstructionToken, '{cmd}')")
        tokens.append("(InstructionTextTokenType.TextToken, ' ')")

        args_text = insn_text[len(cmd):].lstrip()

        if "," in args_text:
            raw_args = args_text.split(",")
        else:
            if len(args_text) == 0:
                raw_args = list()
            else:
                raw_args = [args_text]

        oper_width = 0
        if "." in cmd:
            if cmd.endswith(".b"):
                oper_width = 1
            elif cmd.endswith(".w"):
                oper_width = 2
            elif cmd.endswith(".l"):
                oper_width = 4
            elif cmd == "fmov.s":
                oper_width = 4
            elif cmd == "fmov.d":
                oper_width = 8

        arg_count = len(raw_args)

        arg_objs = list()

        for i, arg in enumerate(raw_args):
            is_ref = False
            is_pair = False
            mod_reg = 0

            # Leading addons
            if arg.startswith("@("):
                arg = arg[2:]
                tokens.append("(InstructionTextTokenType.TextToken, '@(')")
                is_pair = True
                is_ref = True
            if arg.startswith("@@("):
                arg = arg[3:]
                tokens.append("(InstructionTextTokenType.TextToken, '@@(')")
                is_pair = True
                is_ref = True
            if arg.startswith("@-"):
                arg = arg[2:]
                tokens.append("(InstructionTextTokenType.TextToken, '@-')")
                is_ref = True
                assert oper_width != 0, f"@- used without a operation width defined: {arg}"
                mod_reg = -oper_width

            if arg.startswith("@"):
                arg = arg[1:]
                tokens.append("(InstructionTextTokenType.TextToken, '@')")
                is_ref = True

            tailing_tokens = list()
            # Trailing addons
            if is_ref and arg.endswith("+"):
                assert oper_width != 0, f"@**+ used without a operation width defined: {cmd} {arg}"
                mod_reg = oper_width
                arg = arg[:-1]
                tailing_tokens.append("(InstructionTextTokenType.TextToken, '+')")

            if arg.endswith(")"):
                arg = arg[:-1]
                tailing_tokens.append("(InstructionTextTokenType.TextToken, ')')")

            op_type = None
            is_label = False
            op_size = 0

            if arg == "Rn":
                fmt_str = 'R{n}'
                op_type = "OpType.REG"
                tokens.append(f"(InstructionTextTokenType.RegisterToken, '{fmt_str}')")
            elif arg == "Rm":
                fmt_str = 'R{m}'
                op_type = "OpType.REG"
                tokens.append(f"(InstructionTextTokenType.RegisterToken, '{fmt_str}')")
            elif arg == "Rn_BANK":
                fmt_str = 'R{n}_BANK'
                op_type = "OpType.REG"
                tokens.append(f"(InstructionTextTokenType.RegisterToken, '{fmt_str}')")
            elif arg == "Rm_BANK":
                fmt_str = 'R{m}_BANK'
                op_type = "OpType.REG"
                tokens.append(f"(InstructionTextTokenType.RegisterToken, '{fmt_str}')")
            elif arg == "FRn":
                fmt_str = 'FR{n}'
                op_type = "OpType.REG"
                tokens.append(f"(InstructionTextTokenType.RegisterToken, '{fmt_str}')")
            elif arg == "FRm":
                fmt_str = 'FR{m}'
                op_type = "OpType.REG"
                tokens.append(f"(InstructionTextTokenType.RegisterToken, '{fmt_str}')")
            elif arg == "disp" or arg == "disp8" or arg == "disp12" or arg == "label":
                if arg == "disp":
                    if cmd == "bra" or cmd == "bsr":
                        op_size = 2
                    else:
                        op_size = 1
                elif arg == "disp8":
                    op_size = 1
                elif arg == "disp12":
                    op_size = 2
                elif arg == "label":
                    op_size = 2

                fmt_str = '0x{disp:x}'
                op_type = "OpType.DISP"
                if arg == "label":
                    is_label = True
                tokens.append(f"(InstructionTextTokenType.PossibleAddressToken, '{fmt_str}')")
            elif arg == "#imm" or arg == "#imm3" or arg == "#imm20":
                if arg == "#imm" or arg == "#imm3":
                    op_size = 1
                elif arg == "#imm20":
                    op_size = 3

                fmt_str = '0x{imm:x}'
                op_type = "OpType.IMM"
                tokens.append(f"(InstructionTextTokenType.IntegerToken, '{fmt_str}')")
            elif arg in replace_regs:
                op_type = "OpType.REG"
                fmt_str = arg
                tokens.append(f"(InstructionTextTokenType.RegisterToken, '{fmt_str}')")
            else:
                print(f"Unknown arg: {arg}", file=sys.stderr)
                fmt_str = arg
                op_type = "OpType.UNKNOWN"
                tokens.append(f"(InstructionTextTokenType.TextToken, '{fmt_str}')")

            tokens.extend(tailing_tokens)
            if i < (arg_count - 1):
                tokens.append("(InstructionTextTokenType.OperandSeparatorToken, ', ')")

            arg_objs.append(f"Oper({op_type}, '{fmt_str}', {is_ref}, {is_pair}, {mod_reg}, {op_size})")

        nibbles = [bit_pat[0:4], bit_pat[4:8], bit_pat[8:12], bit_pat[12:16]]
        insn_size = 2
        if len(bit_pat) > 16:
            nibbles.extend([bit_pat[16:20], bit_pat[20:24], bit_pat[24:28], bit_pat[28:32]])
            insn_size = 4

        inst = mask = ''
        for b in nibbles:
            if b[0] in '01':
                x = 0
                if b[0] == '1':
                    x = x + 8
                if b[1] == '1':
                    x = x + 4
                if b[2] == '1':
                    x = x + 2
                if b[3] == '1':
                    x = x + 1
                inst = inst + hex(x)[2]
                mask = mask + 'f'
            else:
                inst = inst + '0'
                mask = mask + '0'

        n = nshift = 0
        if bit_pat[4] == 'n':
            n |= 0x0f00
            nshift = 8
        if bit_pat[8] == 'n':
            n |= 0x00f0
            nshift = 4

        m = mshift = 0
        if bit_pat[4] == 'm':
            m |= 0x0f00
            mshift = 8
        elif bit_pat[8] == 'm':
            m |= 0x00f0
            mshift = 4

        imm = ishift = 0
        if bit_pat[8] == 'i':
            imm |= 0x00f0
            ishift = 4
        if bit_pat[12] == 'i':
            imm |= 0x000f
            ishift = 0
        if bit_pat[13] == "i":
            imm |= 0x0007
            ishift = 0

        disp = 0
        if bit_pat[12] == 'd':
            disp |= 0x000f
            if bit_pat[8] == 'd':
                disp |= 0x00f0
                if bit_pat[4] == 'd':
                    disp |= 0x0f00


        if insn_size == 4 and bit_pat[16] == 'd':
            disp |= 0x000f0000
            if bit_pat[20] == 'd':
                disp |= 0x00f00000
                if bit_pat[24] == 'd':
                    disp |= 0x0f000000
                    if bit_pat[28] == 'd':
                        disp |= 0xf0000000

        args_str = ',\n            '.join(arg_objs)
        token_str = ',\n            '.join(tokens)

        fmt = (
            "    {\n"
            f"        'opmask': (0x{inst}, 0x{mask}),\n"
            f"        'm': (0x{m:x}, 0x{mshift:x}),\n"
            f"        'n': (0x{n:x}, 0x{nshift:x}),\n"
            f"        'imm': (0x{imm:x}, 0x{ishift:x}),\n"
            f"        'disp': 0x{disp:x},\n"
            f"        'cmd': '{cmd}',\n"
            f"        'width': {oper_width},\n"
            f"        'size': {insn_size},\n"
            f"        'is_label': {is_label},\n"
            f"        'is_delay': {is_delay},\n"
            "        'args': [\n"
            f"            {args_str}"
            "\n        ],\n"
            "        'tokens': [\n"
            f"            {token_str}"
            "\n        ],\n"
            "    },"
        )
        output.append(fmt)

    output.append(")")
    for elm in output:
        print(elm)

data = fetch()
parse(data)