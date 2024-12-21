import time
import win32api
import win32con
import win32gui
from ctypes import windll, wintypes, WINFUNCTYPE, create_string_buffer, cast, c_int, c_uint
# based on nexus-6's c++ code, converted to python code by AI and modified by me

# Define the types for the SetTimer function parameters
UINT_PTR = c_uint
TIMERPROC = WINFUNCTYPE(None, wintypes.HWND, wintypes.UINT, UINT_PTR, wintypes.DWORD)
# Define the SetTimer function
SetTimer = windll.user32.SetTimer
# Set the argument types and return type
SetTimer.argtypes = [wintypes.HWND, UINT_PTR, wintypes.UINT, TIMERPROC]
SetTimer.restype = UINT_PTR

# Define the TextOutA function prototype
TextOutA = windll.gdi32.TextOutA
# Define the argument types
TextOutA.argtypes = [
    wintypes.HDC,  # hdc
    c_int,  # x
    c_int,  # y
    wintypes.LPCWSTR,  # lpString
    c_int  # c
]
# Define the return type
TextOutA.restype = wintypes.BOOL

def TextOut(hdc, x, y, txt, size):
    if isinstance(txt, str):
        buf = create_string_buffer(txt.encode('utf-8'))
        txt = cast(buf, wintypes.LPCWSTR)
    TextOutA(hdc, x, y, txt, size)

MY_TIMER = 1
time_string = ''

def MyTimerProcCallback(hWnd, uTimerMsg, uTimerID, dwTime):
    # Code for timer MY_TIMER.
    global time_string
    t = time.localtime()
    time_string = time.asctime(t)
    win32gui.InvalidateRect(hWnd, None, 0)

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_PAINT:
        hdc, ps = win32gui.BeginPaint(hwnd)
        TextOut(hdc, 1, 1, time_string, len(time_string))
        win32gui.EndPaint(hwnd, ps)
        return 0
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = WndProc
    wc.lpszClassName = "Center"
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    
    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(wc.lpszClassName, "Center", 
                          win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE, 
                          100, 100, 250, 150, 
                          0, 0, wc.hInstance, None)
    
    # sets up timer function
    MyTimerProc = TIMERPROC(MyTimerProcCallback)
    nTimer = SetTimer(hwnd, MY_TIMER, 1000, MyTimerProc)
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

