import win32gui
import win32api
import win32con
import commctrl
# based on nexus-6's c++ code, converted to python code by AI and modified by me

WC_STATIC = "Static"

# Define control IDs
LEFTLABEL = 1
RIGHTLABEL = 2
COUNTLABEL = 3
TRACKEBARCTL = 4

# Global variables
TrackBar = None
TrackLabel = None

def WndProc(hwnd, msg, wParam, lParam):
    global TrackBar, TrackLabel
    if msg == win32con.WM_CREATE:
        CreateControls(hwnd)
    elif msg == win32con.WM_HSCROLL:
        UpdateLabel()
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def CreateControls(hwnd):
    # Load common control class (ICC_LISTVIEW_CLASSES) - This might need adjustment depending on your needs
    # In Python, InitCommonControlsEx is usually not required and might be handled implicitly by the system.
    # You might need to handle this differently based on what the C++ code is doing.

    LeftLabel = win32gui.CreateWindow(WC_STATIC, "0", win32con.WS_CHILD | win32con.WS_VISIBLE, 0, 0, 10, 30, hwnd, LEFTLABEL, 0, None)
    RightLabel = win32gui.CreateWindow(WC_STATIC, "100", win32con.WS_CHILD | win32con.WS_VISIBLE, 0, 0, 30, 30, hwnd, RIGHTLABEL, 0, None)
    global TrackLabel
    TrackLabel = win32gui.CreateWindow(WC_STATIC, "0", win32con.WS_CHILD | win32con.WS_VISIBLE, 270, 50, 30, 30, hwnd, COUNTLABEL, 0, None)
    global TrackBar
    TrackBar = win32gui.CreateWindow(commctrl.TRACKBAR_CLASS, "Trackbar Control", win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.TBS_AUTOTICKS, 40, 50, 170, 30, hwnd, TRACKEBARCTL, 0, None)

    # Set up trackbar details
    win32gui.SendMessage(TrackBar, commctrl.TBM_SETRANGE,  True, win32api.MAKELONG(0, 100))
    win32gui.SendMessage(TrackBar, commctrl.TBM_SETPAGESIZE, 0,  10)
    win32gui.SendMessage(TrackBar, commctrl.TBM_SETTICFREQ, 10, 0)
    win32gui.SendMessage(TrackBar, commctrl.TBM_SETPOS, False, 0)
    win32gui.SendMessage(TrackBar, commctrl.TBM_SETBUDDY, True, LeftLabel)
    win32gui.SendMessage(TrackBar, commctrl.TBM_SETBUDDY, False, RightLabel)

# Update label when trackbar is changed
def UpdateLabel():
    global TrackBar, TrackLabel
    pos = win32gui.SendMessage(TrackBar, commctrl.TBM_GETPOS, 0, 0)
    buf = str(pos)
    win32gui.SetWindowText(TrackLabel, buf)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "Trackbar"
    wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
    wc.lpfnWndProc = WndProc
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow("Trackbar", "Trackbar control", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE, 100, 100, 350, 180, 0, 0, 0, None)
    
    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32

    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    
    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == '__main__':
    main()