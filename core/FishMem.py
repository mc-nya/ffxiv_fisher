from pymem import Pymem
from core.HandleOperation import get_pid
from pymem.ressources.kernel32 import VirtualProtectEx
from pymem.ressources.structure import MEMORY_PROTECTION
from ctypes import c_ulong, byref,c_ulonglong
class MemReader:
    def __init__(self,hwnd):
        self.FishOffset=int(0x1DD13B0)
        self.MaxGp=int(0x1DAFD20)
        # self.pid=get_pid(hwnd)
        # if isinstance(self.pid,list):
        #     self.pid=min(self.pid)
        # self.pm = Pymem()
        # self.pm.open_process_from_id(int(self.pid))
        self.pm = Pymem('ffxiv_dx11.exe')

    def get_value(self, addr, length):
        base_addr = self.pm.process_base.lpBaseOfDll
        ret=int.from_bytes(self.pm.read_bytes(base_addr+addr, length), byteorder='little')
        return ret

    def _(self, adr, len=4):
        return self.get_value(adr, len)
    def get_fish_status(self):
        return self._(self.FishOffset,2)
    def get_max_gp(self):
        return self._(self.MaxGp,2)
    def get_address(self, adr, len):
        return self._(adr,len)


