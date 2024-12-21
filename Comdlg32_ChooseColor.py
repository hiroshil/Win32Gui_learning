import ctypes
from ctypes import wintypes
import win32api
import win32gui
import win32con
from ctypes import windll, wintypes, WINFUNCTYPE, Structure, POINTER, sizeof, byref, c_bool
# based on nexus-6's c++ code, converted to python code by AI and modified by me

# Define the CHOOSE_COLOR structure
LPCCHOOKPROC = WINFUNCTYPE(
    wintypes.BOOL,  # Return type: BOOL
    wintypes.HWND,  # hwnd
    wintypes.UINT,  # uMsg
    wintypes.WPARAM,  # wParam
    wintypes.LPARAM  # lParam
)
class CHOOSE_COLOR(Structure):
    _fields_ = [
        ("lStructSize", wintypes.DWORD),
        ("hwndOwner", wintypes.HWND),
        ("hInstance", wintypes.HINSTANCE),
        ("rgbResult", wintypes.COLORREF),
        ("lpCustColors", POINTER(wintypes.COLORREF)),
        ("Flags", wintypes.DWORD),
        ("lCustData", wintypes.LPARAM),
        ("lpfnHook", LPCCHOOKPROC),
        ("lpTemplateName", wintypes.LPCSTR)
    ]

# Define the ChooseColor function signature
ChooseColor = windll.comdlg32.ChooseColorW
ChooseColor.argtypes = [POINTER(CHOOSE_COLOR)]
ChooseColor.restype = wintypes.BOOL

ID_BUTTON = 1
gColor = win32api.RGB(255, 255, 255)

def ShowColorDialog(hwnd):
    cc = CHOOSE_COLOR()
    crCustClr = (wintypes.COLORREF * 16)()
    cc.lStructSize = sizeof(cc)
    cc.hwndOwner = hwnd
    cc.lpCustColors = crCustClr
    cc.rgbResult = wintypes.COLORREF()
    cc.Flags = win32con.CC_FULLOPEN | win32con.CC_RGBINIT
    if ChooseColor(byref(cc)):
        return cc.rgbResult
    return gColor

def WndProc(hwnd, msg, wParam, lParam):
    global gColor
    if msg == win32con.WM_PAINT:
        hdc, ps = win32gui.BeginPaint(hwnd)
        win32gui.EndPaint(hwnd, ps)
    elif msg == win32con.WM_ERASEBKGND:
        hBrush = win32gui.CreateSolidBrush(gColor)
        hdc = wParam
        rect = win32gui.GetClientRect(hwnd)
        win32gui.FillRect(hdc, rect, hBrush)
        return 1
    elif msg == win32con.WM_COMMAND:
        gColor = ShowColorDialog(hwnd)
        win32gui.InvalidateRect(hwnd, None, True)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "myWindowClass"
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
    wc.lpfnWndProc = WndProc

    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(wc.lpszClassName, "Color dialog box",
                                  win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                                  0, 0, 700, 200, 0, 0, wc.hInstance, None)

    win32gui.CreateWindow("button", "Color", win32con.WS_VISIBLE | win32con.WS_CHILD,
                           20, 30, 80, 25, hwnd, ID_BUTTON, None, None)
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

