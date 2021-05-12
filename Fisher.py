# -*- coding=utf-8 -*-
from core.SetAdmin import check
from core.HandleOperation import get_window,sendKey,get_pid
from core.FishMem import MemReader
from constant.states import get_states
import atexit
import time
from logic.fish_logic import Fisher
#atexit.register(input, "<<press enter to exit>>")
if __name__ == '__main__':
    import win32gui
    check()
    ffxiv_handle = get_window('最终幻想XIV')
    mem=MemReader(ffxiv_handle)
    fisher=Fisher(mem,ffxiv_handle)
    fisher.run()
    # for i in range(2000):
    #     op_code=hex(mem.get_fish_status())
    #     print(op_code,get_states(op_code))
    #     time.sleep(1)
    