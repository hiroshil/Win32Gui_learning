import win32api
import win32con
import win32gui
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

def TextOut(hdc, x, y, txt):
    buf = create_string_buffer(txt.encode('utf-8'))
    TextOutA(hdc, x, y, cast(buf, wintypes.LPCWSTR), len(txt))

class KeyboardInputDemo:
    def __init__(self):
        self.hwnd = None
        self.key = ""
        self.chr = ""

        wc = win32gui.WNDCLASS()
        wc.style = 0
        wc.lpfnWndProc = self.WndProc
        wc.hInstance = win32api.GetModuleHandle()
        wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW + 1
        wc.lpszClassName = "myWindowClass"

        classAtom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow(
            classAtom,
            "Keyboard Input Demo",
            win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            700,
            350,
            0,
            0,
            win32api.GetModuleHandle(),
            None
        )

        win32gui.PumpMessages()


    def WndProc(self, hwnd, msg, wParam, lParam):
        hdc = win32gui.GetDC(hwnd)

        if msg == win32con.WM_PAINT:
            hdc, ps = win32gui.BeginPaint(hwnd)
            TextOut(hdc, 0, 0, self.key) #displays keystroke value
            TextOut(hdc, 0, 20, self.chr) #displays character
            win32gui.EndPaint(hwnd, ps)
        elif msg == win32con.WM_KEYDOWN:
            self.key = f"KEY is {wParam}"
            
        elif msg == win32con.WM_CHAR:
           self.chr = f"Character is {chr(wParam) if wParam < 256 else ''}"
           win32gui.InvalidateRect(hwnd, None, True)
            
        elif msg == win32con.WM_CLOSE:
            win32gui.DestroyWindow(hwnd)
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
        else:
            return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
        return 0

if __name__ == "__main__":
    KeyboardInputDemo()