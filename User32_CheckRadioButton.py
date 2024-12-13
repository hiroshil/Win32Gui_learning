import win32gui
import win32con
import win32api
from ctypes import windll
from ctypes import wintypes
from ctypes import c_void_p, c_int
# modified from CheckDlgButton example with AI

# Radio button functions
CheckRadioButton = windll.user32.CheckRadioButton
CheckRadioButton.argtypes = [c_void_p, c_int, c_int, c_int]
CheckRadioButton.restype = c_int

title = "Radio Button"

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_COMMAND:
        if wParam == 1:  # First radio button
            CheckRadioButton(hwnd, 1, 2, 1)
            win32gui.SetWindowText(hwnd, "Option 1 selected")
        elif wParam == 2:  # Second radio button
            CheckRadioButton(hwnd, 1, 2, 2)
            win32gui.SetWindowText(hwnd, "Option 2 selected")
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "Radio Button"
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
    wc.lpfnWndProc = WndProc
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    class_atom = win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(class_atom, title,
                                 win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                                 150, 150, 230, 150, 0, 0, wc.hInstance, None)

    win32gui.CreateWindow("button", "Option 1",
                          win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.BS_RADIOBUTTON,
                          20, 20, 185, 35,
                          hwnd, 1, win32api.GetModuleHandle(None), None)

    win32gui.CreateWindow("button", "Option 2",
                          win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.BS_RADIOBUTTON,
                          20, 60, 185, 35,
                          hwnd, 2, win32api.GetModuleHandle(None), None)

    # Set default radio button (Option 1)
    CheckRadioButton(hwnd, 1, 2, 1)
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

