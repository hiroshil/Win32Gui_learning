import win32gui
import win32con
import win32api
from ctypes import windll, wintypes, WINFUNCTYPE, c_size_t, c_ssize_t, c_void_p, c_int
# based on https://github.com/malortie/Tutorials/blob/master/tutorials/cpp/win32/controls/buttons/Button.cpp

WC_BUTTON = "Button"

UINT_PTR = c_size_t
DWORD_PTR = c_size_t
LRESULT = c_ssize_t
SUBCLASSPROC = WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM, UINT_PTR, DWORD_PTR)

SetWindowSubclass = windll.comctl32.SetWindowSubclass
SetWindowSubclass.restype  = wintypes.BOOL
SetWindowSubclass.argtypes = [wintypes.HWND, SUBCLASSPROC, UINT_PTR, DWORD_PTR]
# Radio button functions
CheckRadioButton = windll.user32.CheckRadioButton
CheckRadioButton.argtypes = [c_void_p, c_int, c_int, c_int]
CheckRadioButton.restype = c_int

def LOWORD(dword): return dword & 0x0000ffff
def HIWORD(dword): return dword >> 16

title = "Radio Button"

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_COMMAND:
        pass
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
def GroupBoxProcCallback(hwnd, msg, wParam, lParam, uIdSubclass, dwRefData):
    if msg == win32con.WM_COMMAND:
        wId = LOWORD(wParam)
        wNotify = HIWORD(wParam)
        if wNotify == win32con.BN_CLICKED:
            if wId == 101:  # First radio button
                print("Option 1 selected")
            elif wId == 102:  # Second radio button
                print("Option 2 selected")
            elif wId == 103:  # Third radio button
                print("Option 3 selected")
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "GroupBoxSample"
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
    wc.lpfnWndProc = WndProc
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    class_atom = win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(class_atom, title,
                                win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                                0, 0, 640, 480, 0, 0, wc.hInstance, None)
    
    # Create a group box
    hGroupBox = win32gui.CreateWindow(WC_BUTTON, "Group Box",
                                win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.BS_GROUPBOX,
                                20, 20, 180, 150, hwnd, 0, win32api.GetModuleHandle(None), None)

    GroupBoxProc = SUBCLASSPROC(GroupBoxProcCallback)
    if not SetWindowSubclass(hGroupBox, GroupBoxProc, 0, 0):
        raise Exception("Can't set window subclass for hGroupBox")

    win32gui.CreateWindow(WC_BUTTON, "Option 1",
                          win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.BS_AUTORADIOBUTTON,
                          20, 20, 140, 30,
                          hGroupBox, 101, win32api.GetModuleHandle(None), None)

    win32gui.CreateWindow(WC_BUTTON, "Option 2",
                          win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.BS_AUTORADIOBUTTON,
                          20, 50, 140, 30,
                          hGroupBox, 102, win32api.GetModuleHandle(None), None)
                          
    win32gui.CreateWindow(WC_BUTTON, "Option 3",
                          win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.BS_AUTORADIOBUTTON,
                          20, 80, 140, 30,
                          hGroupBox, 103, win32api.GetModuleHandle(None), None)

    # Set default radio button (Option 1)
    CheckRadioButton(hGroupBox, 101, 103, 102)
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

