import time
import traceback

import win32api
import win32con
import win32gui
# code based https://github.com/Googulator/pypiwin32/blob/master/win32/Demos/desktopmanager.py

def init(user_name):
    windowclassname = 'simple_systray'
    wc = win32gui.WNDCLASS()
    wc.hInstance = win32api.GetModuleHandle()
    wc.lpszClassName = windowclassname
    wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW | win32con.CS_GLOBALCLASS
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW
    wc.lpfnWndProc = wndproc
    windowclass = win32gui.RegisterClass(wc)
    style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
    hwnd = win32gui.CreateWindow(
        windowclass,
        'hello SysTray',
        win32con.WS_SYSMENU,
        0,
        0,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        0,
        0,
        wc.hInstance,
        None)
    win32gui.UpdateWindow(hwnd)
    flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
    global notify_info
    notify_info = (
        hwnd,
        1,
        flags,
        win32con.WM_USER +
        20,
        hicon,
        'Hello, %s' %
        user_name)
    tray_found = 0
    while not tray_found:
        try:
            tray_found = win32gui.FindWindow("Shell_TrayWnd", None)
        except win32gui.error:
            traceback.print_exc
            time.sleep(.5)
    win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, notify_info)
    win32gui.PumpMessages()

def wndproc(hwnd, msg, wp, lp):
    if lp == win32con.WM_RBUTTONDOWN:
        win32gui.SetForegroundWindow(hwnd)

        m = win32gui.CreatePopupMenu()
        menu_items = 4
        for i in range(1, menu_items + 1):
            mf_flags = win32con.MF_STRING
            menu_name = f"menu item {str(i)}"
            if menu_name == "menu item 1":
                mf_flags = mf_flags | win32con.MF_CHECKED
            else:
                mf_flags = mf_flags | win32con.MF_GRAYED | win32con.MF_DISABLED
            win32gui.AppendMenu(m, mf_flags, i, menu_name)
        win32gui.AppendMenu(m, win32con.MF_STRING, menu_items + 1, 'Exit')

        x, y = win32gui.GetCursorPos()
        s = win32gui.TrackPopupMenu(
            m,
            win32con.TPM_LEFTBUTTON | win32con.TPM_RETURNCMD | win32con.TPM_NONOTIFY,
            x,
            y,
            0,
            hwnd,
            None)
        win32gui.PumpWaitingMessages()
        win32gui.DestroyMenu(m)
        if s == menu_items + 1:  # Exit
            global notify_info
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, notify_info)
            win32gui.PostQuitMessage(0)
            return 0
        elif s > 0:
            pass # handle other items
        return 0
    else:
        return win32gui.DefWindowProc(hwnd, msg, wp, lp)

notify_info = tuple()

hinst = win32api.GetModuleHandle(None)
try:
    hicon = win32gui.LoadIcon(hinst, 1)  # python.exe and pythonw.exe
except win32gui.error:
    hicon = win32gui.LoadIcon(hinst, 135)  # pythonwin's icon

init("baka")
