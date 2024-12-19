import win32gui
import win32api
import win32con
from ctypes import windll, wintypes, create_string_buffer, cast, c_int
# based on nexus-6's c++ code, converted to python code by AI and modified by me

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
    buf = create_string_buffer(txt.encode('utf-8'))
    TextOutA(hdc, x, y, cast(buf, wintypes.LPCWSTR), size)

class NonClientAreaMouseClicksDemo:
    def __init__(self):
        self.msg = ""

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
            "Non client area mouse clicks",
            win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            700,
            200,
            0,
            0,
            win32api.GetModuleHandle(),
            None
        )

        win32gui.PumpMessages()


    def WndProc(self, hwnd, message, wParam, lParam):
        hdc = win32gui.GetDC(hwnd)

        if message == win32con.WM_NCHITTEST:
            hittest = win32gui.DefWindowProc(hwnd, message, wParam, lParam)
            if hittest == win32con.HTCAPTION:
                self.msg = "You clicked in the Title Bar "
            elif hittest == win32con.HTCLOSE:
                self.msg = "You clicked the Close Button "
            elif hittest == win32con.HTREDUCE:
                self.msg = "You clicked the Minimize button "
            elif hittest == win32con.HTGROWBOX:
                self.msg = "You clicked the Restore button "
            elif hittest == win32con.HTSYSMENU:
                self.msg = "You clicked in the System menu "
            elif hittest == win32con.HTZOOM:
                self.msg = "You clicked the Restore button "
            elif hittest == win32con.HTRIGHT:
                self.msg = "You clicked the Right border "
            elif hittest == win32con.HTLEFT:
                self.msg = "You clicked the left border "
            elif hittest == win32con.HTBOTTOM:
                self.msg = "You clicked the bottom border "
            elif hittest == win32con.HTTOP:
                self.msg = "You clicked the top border "

        elif message == win32con.WM_NCLBUTTONDOWN:
            strlen = len(self.msg)
            TextOut(hdc, 0, 0, self.msg, strlen)
            return 0

        elif message == win32con.WM_NCLBUTTONDBLCLK:
            win32gui.PostQuitMessage(0)

        elif message == win32con.WM_DESTROY:
            win32gui.DeleteDC(hdc)
            win32gui.PostQuitMessage(0)
            return 0

        return win32gui.DefWindowProc(hwnd, message, wParam, lParam)

if __name__ == "__main__":
    NonClientAreaMouseClicksDemo()