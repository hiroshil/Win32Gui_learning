import win32gui
import win32api
import win32con
from ctypes import windll, wintypes, create_string_buffer, cast, c_int
# based on nexus-6's c++ code, converted to python code by AI and modified by me

# Define the TextOutW function prototype
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
    buf = create_string_buffer(txt.encode('utf-8'))
    TextOutA(hdc, x, y, cast(buf, wintypes.LPCWSTR), size)

def WndProc(hwnd, message, wParam, lParam):
    hdc = win32gui.GetDC(hwnd)
    mousestr = ""
    
    if message == win32con.WM_LBUTTONDOWN:  # deals with left mouse button down
        if wParam & win32con.MK_SHIFT:  # deals with shift key press followed by left button down
            mousestr = f"shift & left button down {win32api.LOWORD(lParam)},{win32api.HIWORD(lParam)}"
            TextOut(hdc, win32api.LOWORD(lParam), win32api.HIWORD(lParam), mousestr, len(mousestr))
        elif wParam & win32con.MK_CONTROL:  # deals with control key press followed by left button down
            mousestr = f"control & left button down {win32api.LOWORD(lParam)},{win32api.HIWORD(lParam)}"
            TextOut(hdc, win32api.LOWORD(lParam), win32api.HIWORD(lParam), mousestr, len(mousestr))
        elif wParam & win32con.MK_RBUTTON:  # deals with right button down followed by left button down
            mousestr = f"left and right button {win32api.LOWORD(lParam)},{win32api.HIWORD(lParam)}"
            TextOut(hdc, win32api.LOWORD(lParam), win32api.HIWORD(lParam), mousestr, len(mousestr))
        else:  # default left mouse button only
            mousestr = f"left button down at {win32api.LOWORD(lParam)},{win32api.HIWORD(lParam)}"
            TextOut(hdc, win32api.LOWORD(lParam), win32api.HIWORD(lParam), mousestr, len(mousestr))
        win32gui.ReleaseDC(hwnd, hdc)

    elif message == win32con.WM_LBUTTONUP:  # deals with left mouse button up
        mousestr = f"left button up at {win32api.LOWORD(lParam)},{win32api.HIWORD(lParam)}"
        TextOut(hdc, win32api.LOWORD(lParam), win32api.HIWORD(lParam), mousestr, len(mousestr))
        win32gui.ReleaseDC(hwnd, hdc)

    elif message == win32con.WM_RBUTTONDOWN:  # deals with right mouse button down
        mousestr = f"right button down at {win32api.LOWORD(lParam)},{win32api.HIWORD(lParam)}"
        TextOut(hdc, win32api.LOWORD(lParam), win32api.HIWORD(lParam), mousestr, len(mousestr))
        win32gui.ReleaseDC(hwnd, hdc)

    elif message == win32con.WM_RBUTTONUP:  # deals with right mouse button up
        mousestr = f"right button up at {win32api.LOWORD(lParam)},{win32api.HIWORD(lParam)}"
        TextOut(hdc, win32api.LOWORD(lParam), win32api.HIWORD(lParam), mousestr, len(mousestr))
        win32gui.ReleaseDC(hwnd, hdc)

    elif message == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0

    return win32gui.DefWindowProc(hwnd, message, wParam, lParam)


wc = win32gui.WNDCLASS()
wc.style = 0
wc.lpfnWndProc = WndProc
wc.hInstance = 0 #hInstance
wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
wc.lpszClassName = "myWindowClass"

atom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(atom, "Displaying Graphics",
                               win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                               win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 700, 300,
                               0, 0, 0, None)  # hInstance, NULL

win32gui.PumpMessages()