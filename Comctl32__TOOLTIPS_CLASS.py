import win32api
import win32con
import win32gui
import commctrl
import sys
from ctypes import wintypes, Structure, sizeof, c_void_p, c_int64, c_uint
# based on nexus-6's c++ code, converted to python code by AI and modified by me

is64bit = "64 bit" in sys.version

if is64bit:
  UINT_PTR = c_int64
else:
  UINT_PTR = c_int

# TOOLINFOA class
class TOOLINFO(Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("hwnd", wintypes.HWND),
        ("uId", UINT_PTR),
        ("rect", wintypes.RECT),
        ("hinst", wintypes.HINSTANCE),
        ("lpszText", wintypes.LPSTR),
        ("lParam", wintypes.LPARAM),
        ("lpReserved", c_void_p),
    ]

WC_BUTTON = "Button"

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_CREATE:
        # load common control class ICC_WIN95_CLASSES
        win32gui.InitCommonControlsEx(commctrl.ICC_WIN95_CLASSES)

        hButton = win32gui.CreateWindow(
            WC_BUTTON, "tooltip test", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER | win32con.BS_PUSHBUTTON,
            10, 10, 150, 25, hwnd, 0, 0, None
        )

        hwndTip = win32gui.CreateWindow(
            commctrl.TOOLTIPS_CLASS, None,
            win32con.WS_POPUP | commctrl.TTS_NOPREFIX | commctrl.TTS_ALWAYSTIP,
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            hwnd, 0, 0, None
        )

        # Associate the tooltip with the tool.
        toolInfoArgs = {"cbSize": sizeof(TOOLINFO),
                    "hwnd": hwnd, "uFlags": commctrl.TTF_IDISHWND | commctrl.TTF_SUBCLASS,
                    "uId": hButton, "lpszText": b"this is a tooltip"}
        toolInfo = TOOLINFO()
        for k, v in toolInfoArgs.items(): setattr(toolInfo, k, v)
        win32gui.SendMessage(hwndTip, commctrl.TTM_ADDTOOL, 0, bytes(toolInfo))

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)


def main():
    wcArgs = {"lpszClassName": "Tooltip",
          "hInstance": 0, # hInstance will be automatically assigned during registration
          "hbrBackground": win32gui.GetSysColorBrush(win32con.COLOR_3DFACE),
          "lpfnWndProc": WndProc,
          "hCursor": win32gui.LoadCursor(0, win32con.IDC_ARROW)}
    wc = win32gui.WNDCLASS()
    for k, v in wcArgs.items(): setattr(wc, k, v)
    
    try:
      win32gui.RegisterClass(wc)
    except Exception as e:
      print(e)
      return

    hwnd = win32gui.CreateWindow(wcArgs["lpszClassName"], "Tooltip", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                           100, 100, 200, 150, 0, 0, 0, None)
    
    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()