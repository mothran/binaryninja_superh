from binaryninja import (
    Architecture,
    CallingConvention,
    RegisterInfo,
    InstructionInfo,
    Endianness,
    InstructionTextToken,
    InstructionTextTokenType,
    BranchType,
    IntrinsicInfo,
    LowLevelILFunction,
    FlagRole,
    LowLevelILFlagCondition,
    LowLevelILLabel,
    log_debug,
    log_error,
    log_info,
    log_warn
)
from binaryninja.types import Type

from .disasm import disasm_single, SHInsn
from .opcodes import OpType, Oper

EM_SH = 42
RSIZE = 4
ISIZE = 2

registers = [
    "R0",
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "R6",
    "R7",
    "R8",
    "R9",
    "R10",
    "R11",
    "R12",
    "R13",
    "R14",
    "R15",
    "FR0",
    "FR1",
    "FR2",
    "FR3",
    "FR4",
    "FR5",
    "FR6",
    "FR7",
    "FR8",
    "FR9",
    "FR10",
    "FR11",
    "FR12",
    "FR13",
    "FR14",
    "FR15",
    "XF0",
    "XF1",
    "XF2",
    "XF3",
    "XF4",
    "XF5",
    "XF6",
    "XF7",
    "XF8",
    "XF9",
    "XF10",
    "XF11",
    "XF12",
    "XF13",
    "XF14",
    "XF15",
    "A0",
    "A1",
    "M0",
    "M1",
]

control_registers = [
    "SR",
    "SSR",
    "SPC",
    "GBR",
    "VBR",
    "SGR",
    "DBR",
    "RE",
    "RS",
    "MOD",
    "TBR",
]

system_registers = [
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

class DefaultCallingConv(CallingConvention):
    name = "Default"
    int_arg_regs = ['R4', 'R5', 'R6', 'R7']
    int_return_reg = 'R0'
    callee_saved_regs = ['R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15']


class Brancher:
    @classmethod
    def find_branches(cls, insn, result: InstructionInfo):
        func_name = 'branch_' + insn.opcode["cmd"].replace("/", "_")
        if hasattr(cls, func_name):
            getattr(cls, func_name)(insn, result)

            if insn.opcode["is_delay"]:
                result.branch_delay = True

    @staticmethod
    def branch_bf(insn, result: InstructionInfo, size=ISIZE):
        result.add_branch(BranchType.TrueBranch, insn.opcode["args"][0].val)
        result.add_branch(BranchType.FalseBranch, insn.addr + size)

    @staticmethod
    def branch_bf_s(insn, result: InstructionInfo):
        Brancher.branch_bf(insn, result, size=4)

    @staticmethod
    def branch_bt(insn, result: InstructionInfo):
        Brancher.branch_bf(insn, result)

    @staticmethod
    def branch_bt_s(insn, result: InstructionInfo):
        Brancher.branch_bf(insn, result, size=4)

    @staticmethod
    def branch_bra(insn, result: InstructionInfo):
        result.add_branch(BranchType.UnconditionalBranch, insn.opcode["args"][0].val)

    @staticmethod
    def branch_braf(insn, result: InstructionInfo):
        result.add_branch(BranchType.IndirectBranch)

    @staticmethod
    def branch_bsr(insn, result: InstructionInfo):
        result.add_branch(BranchType.CallDestination, insn.opcode["args"][0].val)

    @staticmethod
    def branch_bsrf(insn, result: InstructionInfo):
        result.add_branch(BranchType.IndirectBranch)

    @staticmethod
    def branch_jmp(insn, result: InstructionInfo):
        result.add_branch(BranchType.IndirectBranch)

    @staticmethod
    def branch_jsr(insn, result: InstructionInfo):
        result.add_branch(BranchType.IndirectBranch)

    @staticmethod
    def branch_jsr_n(insn, result: InstructionInfo):
        result.add_branch(BranchType.IndirectBranch)

    @staticmethod
    def branch_rts(insn, result: InstructionInfo):
        result.add_branch(BranchType.FunctionReturn)

    @staticmethod
    def branch_rts_n(insn, result: InstructionInfo):
        result.add_branch(BranchType.FunctionReturn)

    @staticmethod
    def branch_rtv_n(insn, result: InstructionInfo):
        result.add_branch(BranchType.FunctionReturn)

class Lifter:
    @classmethod
    def lift(cls, il: LowLevelILFunction, insn: SHInsn):
        func_name = 'lift_' + insn.opcode["cmd"].replace("/", "_").replace(".", "_")
        if hasattr(cls, func_name):
            getattr(cls, func_name)(il, insn)
        else:
            il.append(il.unimplemented())

    @staticmethod
    def _lift_op(il: LowLevelILFunction, insn: SHInsn, op: Oper, sign_ext=False):
        il_op = None

        if op.type == OpType.REG:
            if op.reg == "PC":
                il_op = il.const(RSIZE, insn.addr)
            else:
                il_op = il.reg(RSIZE, op.reg)
        elif op.type == OpType.IMM or op.type == OpType.DISP:
            assert op.size != 0, f"Invalid instruction at: 0x{insn.addr:x}"

            if op.type == OpType.DISP and op.is_ref and op.is_pair:
                # Fetch the next part of the pair
                next_op = None
                for i, cur_op in enumerate(insn.opcode["args"]):
                    if cur_op.is_pair:
                        next_op = insn.opcode["args"][i + 1]
                        break
                assert next_op is not None, f"Invalid instruction at: 0x{insn.addr:x}"
                assert next_op.type == OpType.REG, f"Invalid instruction at: 0x{insn.addr:x}"

                if next_op.reg == "PC":
                    cur_il = il.shift_left(RSIZE,
                        il.const(RSIZE, op.val),
                        il.const(RSIZE, int(insn.opcode['width'] / 2))
                    )

                    if insn.opcode["width"] == 4:
                        next_il = il.and_expr(RSIZE,
                            il.const(RSIZE, insn.addr),
                            il.const(RSIZE, 0xFFFFFFFC)
                        )
                    else:
                        next_il = il.const(RSIZE, insn.addr)

                    next_il = il.add(RSIZE,
                        next_il,
                        il.const(RSIZE, 4)
                    )

                else:
                    cur_il = il.const(op.size, op.val)
                    next_il = il.reg(RSIZE, next_op.reg)

                il_op = il.add(RSIZE,
                    cur_il,
                    next_il
                )
            else:
                il_op = il.const(op.size, op.val)

        if sign_ext:
            il_op = il.sign_extend(RSIZE, il_op)

        return il_op

    @staticmethod
    def lift_mov(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 2, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        op_2 = insn.opcode["args"][1]

        extend = False
        if op_1.type == OpType.IMM:
            extend = True

        il.append(
            il.set_reg(RSIZE,
                op_2.reg,
                Lifter._lift_op(il, insn, op_1, extend)
            )
        )

    @staticmethod
    def lift_movi20(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 2, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        op_2 = insn.opcode["args"][1]

        il.append(
            il.set_reg(RSIZE,
                op_2.reg,
                Lifter._lift_op(il, insn, op_1, True)
            )
        )

    @staticmethod
    def lift_movi20s(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 2, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        op_2 = insn.opcode["args"][1]

        assert op_1.type == OpType.IMM, f"Invalid instruction at: 0x{insn.addr:x}"
        assert op_1.size != 0, f"Invalid instruction at: 0x{insn.addr:x}"

        il.append(
            il.set_reg(RSIZE,
                op_2.reg,
                il.sign_extend(RSIZE,
                    il.shift_left(op_1.size,
                        il.const(op_1.size, op_1.val),
                        il.const(1, 8)
                    )
                )
            )
        )

    @staticmethod
    def lift_mova(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 3, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        op_2 = insn.opcode["args"][1]
        op_3 = insn.opcode["args"][2]

        il.append(
            il.set_reg(RSIZE,
                op_3.reg,
                il.add(RSIZE,
                    il.and_expr(RSIZE,
                        il.reg(RSIZE, op_2.reg),
                        il.const(RSIZE, 0xFFFFFFFC)
                    ),
                    il.add(RSIZE,
                        il.const(RSIZE, 4),
                        il.shift_left(RSIZE,
                            il.const(RSIZE, op_1.val),
                            il.const(RSIZE, 2)
                        )
                    )
                )
            )
        )

    @staticmethod
    def lift_mov_b(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) > 1, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        if op_1.is_pair:
            op_2 = insn.opcode["args"][2]
        else:
            op_2 = insn.opcode["args"][1]

        extra_op = None

        if op_1.is_ref:
            il_op = il.set_reg(RSIZE,
                op_2.reg,
                il.load(insn.opcode["width"],
                    Lifter._lift_op(il, insn, op_1)
                )
            )

            if op_1.mod_reg != 0:
                if op_1.type == OpType.REG and op_2.type == OpType.REG and op_1.mod_reg > 0:
                    extra_op = None
                else:
                    extra_op = il.set_reg(RSIZE,
                        op_1.reg,
                        il.add(RSIZE,
                            il.reg(RSIZE, op_1.reg),
                            il.const(RSIZE, op_1.mod_reg)
                        )
                    )

        elif op_2.is_ref:
            il_op = il.store(insn.opcode["width"],
                Lifter._lift_op(il, insn, op_2),
                Lifter._lift_op(il, insn, op_1)
            )

            if op_2.mod_reg != 0:
                extra_op = il.set_reg(RSIZE,
                    op_2.reg,
                    il.add(RSIZE,
                        il.reg(RSIZE, op_2.reg),
                        il.const(RSIZE, op_2.mod_reg)
                    )
                )

        else:
            assert False, f"Invalid instruction at: 0x{insn.addr:x}"

        il.append(il_op)

        if extra_op is not None:
            il.append(extra_op)

    @staticmethod
    def lift_mov_w(il: LowLevelILFunction, insn: SHInsn):
        Lifter.lift_mov_b(il, insn)

    @staticmethod
    def lift_mov_l(il: LowLevelILFunction, insn: SHInsn):
        Lifter.lift_mov_b(il, insn)

    @staticmethod
    def lift_sub(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 2, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        op_2 = insn.opcode["args"][1]

        il.append(
            il.set_reg(RSIZE,
                op_2.reg,
                il.sub(RSIZE,
                    il.reg(RSIZE, op_1.reg),
                    il.reg(RSIZE, op_2.reg),
                )
            )
        )

    @staticmethod
    def lift_add(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 2, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        op_2 = insn.opcode["args"][1]

        il.append(
            il.set_reg(RSIZE,
                op_2.reg,
                il.add(RSIZE,
                    Lifter._lift_op(il, insn, op_1, True),
                    il.reg(RSIZE, op_2.reg),
                )
            )
        )

    @staticmethod
    def lift_cmp_eq(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 2, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        op_2 = insn.opcode["args"][1]

        extend = False
        if op_1.type == OpType.IMM:
            extend = True

        t = LowLevelILLabel()
        f = LowLevelILLabel()
        next_insn = LowLevelILLabel()

        il.append(
            il.if_expr(
                il.compare_equal(RSIZE,
                    Lifter._lift_op(il, insn, op_1, sign_ext=extend),
                    Lifter._lift_op(il, insn, op_2)
                ),
                t,
                f
            )
        )

        il.mark_label(t)
        il.append(
            il.set_flag('t', il.const(0, 1))
        )
        il.append(
            il.goto(next_insn)
        )

        il.mark_label(f)
        il.append(
            il.set_flag('t', il.const(0, 0))
        )

        il.mark_label(next_insn)


    @staticmethod
    def lift_tst(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 2, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]
        op_2 = insn.opcode["args"][1]

        t = LowLevelILLabel()
        f = LowLevelILLabel()
        next_insn = LowLevelILLabel()

        il.append(
            il.if_expr(
                il.compare_equal(RSIZE,
                    il.and_expr(RSIZE,
                        Lifter._lift_op(il, insn, op_1),
                        Lifter._lift_op(il, insn, op_2)
                    ),
                    il.const(RSIZE, 0)
                ),
                t,
                f
            )
        )

        il.mark_label(t)
        il.append(
            il.set_flag('t', il.const(0, 1))
        )
        il.append(
            il.goto(next_insn)
        )

        il.mark_label(f)
        il.append(
            il.set_flag('t', il.const(0, 0))
        )

        il.mark_label(next_insn)

    @staticmethod
    def lift_bf(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 1, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]

        t = il.get_label_for_address(Architecture["superh"], op_1.val)

        if t is None:
            t = LowLevelILLabel()
            indirect = True
        else:
            indirect = False

        f = LowLevelILLabel()

        il.append(
            il.if_expr(
                il.compare_equal(0,
                    il.flag("t"),
                    il.const(0, 0)
                ),
                t,
                f
            )
        )

        if indirect:
            il.mark_label(t)

            il.append(
                il.jump(il.const(RSIZE, op_1.val))
            )

        il.mark_label(f)

    @staticmethod
    def lift_bf_s(il: LowLevelILFunction, insn: SHInsn):
        Lifter.lift_bf(il, insn)

    @staticmethod
    def lift_bt(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 1, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]

        t = il.get_label_for_address(Architecture["superh"], op_1.val)

        if t is None:
            t = LowLevelILLabel()
            indirect = True
        else:
            indirect = False

        f = LowLevelILLabel()

        il.append(
            il.if_expr(
                il.flag("t"),
                t,
                f
            )
        )

        if indirect:
            il.mark_label(t)

            il.append(
                il.jump(il.const(RSIZE, op_1.val))
            )

        il.mark_label(f)

    @staticmethod
    def lift_bt_s(il: LowLevelILFunction, insn: SHInsn):
        Lifter.lift_bt(il, insn)


    @staticmethod
    def lift_bra(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 1, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]

        il.append(
            il.jump(il.const(RSIZE, op_1.val))
        )

    @staticmethod
    def lift_jsr(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 1, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]

        il.append(
            il.call(
                Lifter._lift_op(il, insn, op_1)
            )
        )

    @staticmethod
    def lift_bsrf(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 1, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]

        il.append(
            il.call(
                il.add(RSIZE,
                    il.const(RSIZE, insn.addr),
                    il.add(RSIZE,
                        il.reg(RSIZE, op_1.reg),
                        il.const(RSIZE, 4)
                    )
                )
            )
        )

    @staticmethod
    def lift_jmp(il: LowLevelILFunction, insn: SHInsn):
        assert len(insn.opcode["args"]) == 1, f"Invalid instruction at: 0x{insn.addr:x}"

        op_1 = insn.opcode["args"][0]

        il.append(
            il.jump(
                Lifter._lift_op(il, insn, op_1)
            )
        )

    @staticmethod
    def lift_nop(il: LowLevelILFunction, insn: SHInsn):
        il.append(il.nop())
    @staticmethod
    def lift_nopx(il: LowLevelILFunction, insn: SHInsn):
        il.append(il.nop())
    @staticmethod
    def lift_nopy(il: LowLevelILFunction, insn: SHInsn):
        il.append(il.nop())


class SuperH(Architecture):
    name = "superh"
    endianness = Endianness.LittleEndian
    address_size = 4
    default_int_size = 2
    max_instr_length = 4
    instr_alignment = 2

    regs = dict()

    for r in registers:
        regs[r] = RegisterInfo(r, RSIZE)

    for r in system_registers:
        regs[r] = RegisterInfo(r, RSIZE)

    for r in control_registers:
        regs[r] = RegisterInfo(r, RSIZE)

    flags = ['t']
    flag_roles = {
        't': FlagRole.SpecialFlagRole
    }

    stack_pointer = 'R15'
    link_reg = 'PR'

    system_regs = system_registers + control_registers

    def __init__(self):
        super().__init__()

    def get_instruction_info(self, data, addr):
        result = InstructionInfo()
        result.length = ISIZE

        insn = disasm_single(data, addr)

        if not insn:
            return result

        result.length = insn.size
        Brancher.find_branches(insn, result)

        return result

    def get_instruction_text(self, data, addr):
        tokens = list()
        insn = disasm_single(data, addr)

        if not insn:
            tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, "<unknown>"))
            return tokens, ISIZE

        for token_type, token_text in insn.tokens:
            tokens.append(InstructionTextToken(token_type, token_text))

        return tokens, insn.size

    def get_instruction_low_level_il(self, data, addr, il):
        insn = disasm_single(data, addr)

        if not insn:
            il.append(il.unimplemented())
            return None

        Lifter.lift(il, insn)

        return insn.size
