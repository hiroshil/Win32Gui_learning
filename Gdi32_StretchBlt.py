import win32gui
import win32api
import win32con
# based on nexus-6's c++ code, converted to python code by AI

def WndProc(hwnd, msg, wParam, lParam):

    if msg == win32con.WM_LBUTTONDOWN:
        maxX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        maxY = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        width = 0
        height = 0
        rect = win32gui.GetWindowRect(hwnd)

        if rect:
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

        mhdc = win32gui.GetWindowDC(0)  # creates a main windows device context
        hdc = win32gui.GetDC(hwnd)  # creates application window device context
        hbit = win32gui.CreateCompatibleBitmap(mhdc, maxX, maxY)  # create screen device context compatible bitmap
        win32gui.StretchBlt(hdc, 0, 0, width, height, mhdc, 0, 0, maxX, maxY, win32con.MERGECOPY)  # copies main window bitmap to application screen
        win32gui.ReleaseDC(hwnd, mhdc)
        win32gui.ReleaseDC(hwnd, hdc)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0

    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wc.lpfnWndProc = WndProc
    wc.lpszClassName = "Screen copy"
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_BTNFACE)
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(wc.lpszClassName, "screen copy", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE, 100, 100, 390, 350, None, None, wc.hInstance, None)

    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

