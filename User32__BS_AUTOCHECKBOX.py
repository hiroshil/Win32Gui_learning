import win32gui
import win32api
import win32con
from ctypes import windll, wintypes, c_int
# based on nexus-6's c++ code, converted to python code by AI

WC_BUTTON = "Button"
ID_BLUE = 1
ID_GREEN = 2
ID_RED = 3

IsDlgButtonChecked = windll.user32.IsDlgButtonChecked
IsDlgButtonChecked.argtypes = [wintypes.HWND, c_int]
IsDlgButtonChecked.restype = c_int

def WndProc(hwnd, msg, wParam, lParam):
    global red, green, blue

    if msg == win32con.WM_COMMAND:
        if win32api.HIWORD(wParam) == win32con.BN_CLICKED:
            if win32api.LOWORD(wParam) == ID_BLUE:
                checked = IsDlgButtonChecked(hwnd, ID_BLUE)
                blue = checked * 255
            elif win32api.LOWORD(wParam) == ID_GREEN:
                checked = IsDlgButtonChecked(hwnd, ID_GREEN)
                green = checked * 255
            elif win32api.LOWORD(wParam) == ID_RED:
                checked = IsDlgButtonChecked(hwnd, ID_RED)
                red = checked * 255
            win32gui.InvalidateRect(hwnd, None, True)

    elif msg == win32con.WM_PAINT:
        hdc, ps = win32gui.BeginPaint(hwnd)
        bk_color = win32api.RGB(red, green, blue)
        hBrush = win32gui.CreateSolidBrush(bk_color)
        theRect = win32gui.GetClientRect(hwnd)
        win32gui.FillRect(hdc, theRect, hBrush)
        win32gui.EndPaint(hwnd, ps)
        win32gui.DeleteObject(hBrush)
        win32gui.ReleaseDC(hwnd, hdc)

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)


wc = win32gui.WNDCLASS()
wc.style = 0
wc.lpfnWndProc = WndProc
wc.hInstance = 0 #hInstance
wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
wc.lpszClassName = "myWindowClass"

atom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(atom, "Check Box Demo",
                               win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                               win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 700, 350,
                               0, 0, 0, None)  # hInstance, NULL
red = 0
green = 0
blue = 0
checked = None
win32gui.CreateWindow("button", "Blue", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_AUTOCHECKBOX, 200, 60, 70, 30, hwnd, ID_BLUE, None, None)
win32gui.CreateWindow("button", "Green", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_AUTOCHECKBOX, 270, 60, 70, 30, hwnd, ID_GREEN, None, None)
win32gui.CreateWindow("button", "Red", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_AUTOCHECKBOX, 340, 60, 70, 30, hwnd, ID_RED, None, None)

win32gui.PumpMessages()