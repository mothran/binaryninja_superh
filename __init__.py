from binaryninja import Architecture, BinaryViewType, enums

from .superh import SuperH, EM_SH, DefaultCallingConv

SuperH.register()
arch = Architecture['superh']
arch.register_calling_convention(DefaultCallingConv(arch, 'default'))
arch.standalone_platform.default_calling_convention = arch.calling_conventions['default']

BinaryViewType['ELF'].register_arch(
    EM_SH,
    enums.Endianness.LittleEndian,
    arch
)