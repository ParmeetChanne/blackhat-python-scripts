import volatility.addrspace as addrspace
import volatility.commands as commands
import sys
import struct
import volatility.conf as conf
import volatility.registry as registry

memory_file = "WindowsXPSP2.vmem"
sys.path.append("/Users/justin/Downloads/volatility-2.3.1")

registry.PluginImporter()
config = conf.ConfObject()


config.parse_options()
config.PROFILE = "WinXPSP2x86"
config.LOCATION = "file://%s" % memory_file

registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)

registry = RegistryApi(config)
registry.populate_offsets()

sam_offset = None
sys.offset = None
for offset in registry.all_offsets:
    if registry.all_offsets[offset].endswith("\\SAM"):
        sam_offset = offset
        print("[*] SAM: 0x%08x" % offset)

    if registry.all_offsets[offset].endswith("\\system"):
        sys.offset = offset
        print("[*] System: 0x%08x" % offset)

    if sam_offset is not None and sys_offset is not None:
        config.sys_offset = sys_offset
        config.sam_offset = sam_offset

        hashdump = HashDump(config)

        for hash in hashdump.calculate():
            print(hash)

        break

if sam_offset is NNone or sys_offset is None:
    print("[*] Failed to find the system or SAM offsets.")
