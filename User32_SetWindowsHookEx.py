import win32api
import win32gui
import win32con
from ctypes import windll, wintypes, WINFUNCTYPE, c_uint, c_int, c_ssize_t
# based on nexus-6's c++ code, converted to python code by AI and modified by me

# Define the types for the SetTimer function parameters
UINT_PTR = c_uint
LRESULT = c_ssize_t
TIMERPROC = WINFUNCTYPE(None, wintypes.HWND, wintypes.UINT, UINT_PTR, wintypes.DWORD)
HOOKPROC = WINFUNCTYPE(LRESULT, c_int, wintypes.WPARAM, wintypes.LPARAM)

# Define the SetTimer function
SetTimer = windll.user32.SetTimer
# Set the argument types and return type
SetTimer.argtypes = [wintypes.HWND, UINT_PTR, wintypes.UINT, TIMERPROC]
SetTimer.restype = UINT_PTR

# Define the SetWindowsHookEx function
SetWindowsHookEx = windll.user32.SetWindowsHookExA
SetWindowsHookEx.argtypes = [c_int, HOOKPROC, wintypes.HINSTANCE, wintypes.DWORD]
SetWindowsHookEx.restype = wintypes.HHOOK

# Define the UnhookWindowsHookEx function
UnhookWindowsHookEx = windll.user32.UnhookWindowsHookEx
UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
UnhookWindowsHookEx.restype = wintypes.BOOL

# Define the CallNextHookEx function
CallNextHookEx = windll.user32.CallNextHookEx
CallNextHookEx.argtypes = [wintypes.HHOOK, c_int, wintypes.WPARAM, wintypes.LPARAM]
CallNextHookEx.restype = LRESULT

# Define necessary types
LPCSTR = wintypes.LPCSTR
DWORD = wintypes.DWORD
HFONT = wintypes.HANDLE
# Define the CreateFontA function signature
CreateFont = windll.gdi32.CreateFontA
CreateFont.argtypes = [
    c_int,  # cHeight
    c_int,  # cWidth
    c_int,  # cEscapement
    c_int,  # cOrientation
    c_int,  # cWeight
    DWORD,  # bItalic
    DWORD,  # bUnderline
    DWORD,  # bStrikeOut
    DWORD,  # iCharSet
    DWORD,  # iOutPrecision
    DWORD,  # iClipPrecision
    DWORD,  # iQuality
    DWORD,  # iPitchAndFamily
    LPCSTR  # pszFaceName
]
CreateFont.restype = HFONT



MY_TIMER = 1
# Initialize countdown
countdown = [10]  # Using a list to allow modification in nested function

# Process countdown timer event
def MyTimerProc(hWnd, uTimerMsg, uTimerID, dwTime):
    countdown[0] -= 1
    win32gui.SetWindowText(staticbox, str(countdown[0]))
    if not countdown[0]:
        win32api.PostQuitMessage(0)

# Customized windows procedure for handling message box behavior
def CBTProc(nCode, wParam, lParam):
    global staticbox
    if nCode == win32con.HCBT_ACTIVATE:
        hwnd = wParam
        # Create messagebox contents
        staticbox = win32gui.CreateWindow(
            "STATIC", 
            str(countdown[0]), 
            win32con.WS_CHILD | win32con.WS_VISIBLE, 
            5, 5, 35, 35, 
            hwnd, 
            1, 
            None, 
            None
        )  # Static control
        font = CreateFont(25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"Times New Roman")
        win32gui.SendMessage(staticbox, win32con.WM_SETFONT, font, True)
        nTimer = SetTimer(hwnd, MY_TIMER, 1000, MyTimerProcCallback)
        return 0
    return CallNextHookEx(hMsgBoxHook, nCode, wParam, lParam)

def main():
    global hMsgBoxHook, MyTimerProcCallback
    MyTimerProcCallback = TIMERPROC(MyTimerProc)
    CBTProcCallback = HOOKPROC(CBTProc)
    
    # Window hook allows the application to intercept message-box creation, and customize it
    hMsgBoxHook = SetWindowsHookEx(win32con.WH_CBT, CBTProcCallback, None, win32api.GetCurrentThreadId())
    # Display a standard message box
    win32gui.MessageBox(None, str(), "Self terminating message box", int())
    # Remove the window hook
    UnhookWindowsHookEx(hMsgBoxHook)

if __name__ == "__main__":
    main()

