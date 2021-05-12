import win32gui,win32api,win32con,win32process
import time
hwnd_title = dict()
def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})

def get_window(name):
    win32gui.EnumWindows(get_all_hwnd, 0)
    handle=0
    for h,t in hwnd_title.items():
        if t==name:
            handle=h
    assert(handle!=0)
    title = win32gui.GetWindowText(handle)
    clsname = win32gui.GetClassName(handle)
    print('Get window', title,clsname)
    return handle

def sendKey(handle,key):
    win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord(key), 0)
    win32api.PostMessage(handle, win32con.WM_KEYUP, ord(key), 0)
    time.sleep(0.01)
    win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord(key), 0)
    win32api.PostMessage(handle, win32con.WM_KEYUP, ord(key), 0)
    time.sleep(0.01)
    win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord(key), 0)
    win32api.PostMessage(handle, win32con.WM_KEYUP, ord(key), 0)

def get_pid(hwnd):
    return win32process.GetWindowThreadProcessId(hwnd)