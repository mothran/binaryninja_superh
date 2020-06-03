import sys
from disasm import disasm_single, SHInsn

addr = 0x5000
raw_insn = bytes.fromhex(sys.argv[1])
insn: SHInsn = disasm_single(raw_insn, addr)

if not insn:
    print("Failed to disassemble")
    sys.exit(0)

print(insn.insn_str)