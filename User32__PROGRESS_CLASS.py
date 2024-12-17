import win32gui
import win32con
import win32api
import commctrl
# converted to python from https://github.com/malortie/Tutorials/blob/master/tutorials/cpp/win32/controls/progressbar/ProgressBar.cpp
# by AI

# Constants
ID_DEFAULTPROGRESSCTRL = 401
ID_SMOOTHPROGRESSCTRL = 402
ID_VERTICALPROGRESSCTRL = 403

# Window Procedure
def WndProc(hWnd, message, wParam, lParam):
    if message == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    else:
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)
    return 0

# Main function (equivalent to WinMain)
def main():
    # Initialize common controls
    win32gui.InitCommonControlsEx(commctrl.ICC_PROGRESS_CLASS)

    # Register window class
    wc = win32gui.WNDCLASS()
    wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wc.lpfnWndProc = WndProc
    wc.hInstance = win32gui.GetModuleHandle(None)
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.lpszClassName = "PROGRESSBARSAMPLE"

    # Register the Window Class
    if not win32gui.RegisterClass(wc):
        raise RuntimeError('Failed to register window class')

    # Create the window
    hWnd = win32gui.CreateWindowEx(
        0,
        wc.lpszClassName,
        "ProgressBar samples",
        win32con.WS_OVERLAPPEDWINDOW,
        0, 0, 640, 480,
        None, None, wc.hInstance, None
    )

    if not hWnd:
        raise RuntimeError('Failed to create window')

    # Create default progress bar
    hDefaultProgressCtrl = win32gui.CreateWindowEx(
        0,
        commctrl.PROGRESS_CLASS,
        "",
        win32con.WS_CHILD | win32con.WS_VISIBLE,
        20, 20, 450, 30,
        hWnd, ID_DEFAULTPROGRESSCTRL, wc.hInstance, None
    )
    win32gui.SendMessage(hDefaultProgressCtrl, commctrl.PBM_SETPOS, 40, 0)

    # Create smooth progress bar
    hSmoothProgressCtrl = win32gui.CreateWindowEx(
        0,
        commctrl.PROGRESS_CLASS,
        "",
        win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.PBS_SMOOTH,
        20, 60, 450, 30,
        hWnd, ID_SMOOTHPROGRESSCTRL, wc.hInstance, None
    )
    win32gui.SendMessage(hSmoothProgressCtrl, commctrl.PBM_SETPOS, 40, 0)

    # Create vertical progress bar
    hVerticalProgressCtrl = win32gui.CreateWindowEx(
        0,
        commctrl.PROGRESS_CLASS,
        "",
        win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.PBS_VERTICAL,
        20, 100, 30, 100,
        hWnd, ID_VERTICALPROGRESSCTRL, wc.hInstance, None
    )
    win32gui.SendMessage(hVerticalProgressCtrl, commctrl.PBM_SETPOS, 40, 0)

    # Show & update the window
    win32gui.ShowWindow(hWnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hWnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

