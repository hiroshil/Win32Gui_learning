import win32gui
import win32con
import win32api
from ctypes import windll
from ctypes import wintypes
from ctypes import c_void_p, c_int
# based on some code generated from colab AI and https://stackoverflow.com/questions/24065214/how-to-make-checkbox-in-win32

CheckDlgButton = windll.user32.CheckDlgButton
CheckDlgButton.argtypes = [c_void_p, c_int, c_int]
CheckDlgButton.restype = c_int
IsDlgButtonChecked = windll.user32.IsDlgButtonChecked
IsDlgButtonChecked.argtypes = [wintypes.HWND, c_int]
IsDlgButtonChecked.restype = c_int

title = "Check Box"

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_COMMAND:
        checked = IsDlgButtonChecked(hwnd, 1)
        if checked:
            CheckDlgButton(hwnd, 1, win32con.BST_UNCHECKED)
            win32gui.SetWindowText(hwnd, "")
        else:
            CheckDlgButton(hwnd, 1, win32con.BST_CHECKED)
            win32gui.SetWindowText(hwnd, title)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "Check Box"
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
    wc.lpfnWndProc = WndProc
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    class_atom = win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(class_atom, title,
                                 win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                                 150, 150, 230, 150, 0, 0, wc.hInstance, None)

    win32gui.CreateWindow("button", "Show Title",
                              win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.BS_CHECKBOX,
                              20, 20, 185, 35,
                              hwnd, 1, win32api.GetModuleHandle(None), None)
    CheckDlgButton(hwnd, 1, win32con.BST_CHECKED)
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

