import win32api
import win32con
import win32gui
import commctrl
import array
# based on nexus-6's c++ code, converted to python code by AI and modified by me

# Define constants
IDC_STATUSBAR = 100
IDI_ICON = 101

hWndStatusBar = None

def WndProc(hWnd, Msg, wParam, lParam):
    global hWndStatusBar
    
    if Msg == win32con.WM_CREATE:
        hWndStatusBar = win32gui.CreateWindow(commctrl.STATUSCLASSNAME,
                                                None,
                                                win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.SBARS_SIZEGRIP,
                                                0, 0, 0, 0,
                                                hWnd,
                                                IDC_STATUSBAR,
                                                win32api.GetModuleHandle(None),
                                                None)

        if not hWndStatusBar:
            win32api.MessageBox(0, "Failed To Create The Status Bar", "Error", win32con.MB_OK | win32con.MB_ICONERROR)
            return 0

        iStatusWidths = [150, 310, -1]
        
        # Sets the number of parts in a status window and the coordinate of the right edge of each part.
        buf = array.array('i', iStatusWidths).tobytes()
        win32gui.SendMessage(hWndStatusBar, commctrl.SB_SETPARTS, 3, buf)
        
        # The SB_SETTEXT message sets the text in a status window.
        win32gui.SendMessage(hWndStatusBar, commctrl.SB_SETTEXT, 0, b"Status Bar Cell  1 width 120")
        win32gui.SendMessage(hWndStatusBar, commctrl.SB_SETTEXT, 1, b"Status Bar Cell 2 width 130")
        win32gui.SendMessage(hWndStatusBar, commctrl.SB_SETTEXT, 2, b"Status Bar Cell 3 width remaining space")
        
        win32gui.ShowWindow(hWndStatusBar, win32con.SW_SHOW)

    elif Msg == win32con.WM_SIZE:
        win32gui.SendMessage(hWndStatusBar, win32con.WM_SIZE, 0, 0)

    elif Msg == win32con.WM_CLOSE:
        win32gui.DestroyWindow(hWnd)
    
    elif Msg == win32con.WM_DESTROY:
        win32api.PostQuitMessage(0)
    
    else:
        return win32gui.DefWindowProc(hWnd, Msg, wParam, lParam)

    return 0

def main():
    # Initialize common controls
    win32gui.InitCommonControls()

    wc = win32gui.WNDCLASS()
    wc.style = 0
    wc.lpfnWndProc = WndProc
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)#Requires resource compilation
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.lpszClassName = "MainWindowClass"

    if not win32gui.RegisterClass(wc):
        win32api.MessageBox(0, "Failed To Register The Window Class.", "Error", win32con.MB_OK | win32con.MB_ICONERROR)
        return 0
    
    hWnd = win32gui.CreateWindow("MainWindowClass", "Status Bar", win32con.WS_OVERLAPPEDWINDOW, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 555, 120, 0, 0, wc.hInstance, None)
    
    if not hWnd:
        win32api.MessageBox(0, "Window Creation Failed.", "Error", win32con.MB_OK | win32con.MB_ICONERROR)
        return 0

    win32gui.SendMessage(hWnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    win32gui.ShowWindow(hWnd, win32con.SW_SHOW)
    win32gui.UpdateWindow(hWnd)
    
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()