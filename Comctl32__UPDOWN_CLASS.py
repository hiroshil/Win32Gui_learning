import win32gui
import win32con
import win32api
import win32gui_struct
import commctrl
# based on nexus-6's c++ code, converted to python code by AI and modified by me

WC_EDIT = "Edit"
WC_STATIC = "Static"

ID_UPDOWN = 1
ID_EDIT = 2
ID_STATIC = 3
UD_MAX_POS = 30
UD_MIN_POS = 0

hUpDown = None
hEdit = None
hStatic = None

def WndProc(hwnd, msg, wParam, lParam):
    global hUpDown, hEdit, hStatic

    if msg == win32con.WM_CREATE:
        CreateControls(hwnd)
    elif msg == win32con.WM_NOTIFY:
        # i'm too lazy to write an unpack function so I picked a random function from the library to use, not recommended to follow
        lpnmud = win32gui_struct.UnpackNMITEMACTIVATE(lParam)
        iPos = lpnmud.iItem
        iDelta = lpnmud.iSubItem
        code = lpnmud.code
        if code == commctrl.UDN_DELTAPOS:
            value = iPos + iDelta
            if value < UD_MIN_POS:
                value = UD_MIN_POS
            if value > UD_MAX_POS:
                value = UD_MAX_POS
            buf = f"{value}"
            win32gui.SetWindowText(hStatic, buf)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def CreateControls(hwnd):
    # Load common control class ICC_UPDOWN_CLASS from the dynamic-link library (DLL).
    win32gui.InitCommonControlsEx(commctrl.ICC_UPDOWN_CLASS)

    # Create spinner window
    global hUpDown, hEdit, hStatic
    hUpDown = win32gui.CreateWindow(
        commctrl.UPDOWN_CLASS, 
        None, 
        win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.UDS_SETBUDDYINT | commctrl.UDS_ALIGNRIGHT, 
        0, 0, 120, 120, 
        hwnd, 
        ID_UPDOWN, 
        None, 
        None
    )
    # Create buddy edit window
    hEdit = win32gui.CreateWindow(
        WC_EDIT, 
        None, 
        win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.ES_RIGHT, 
        15, 15, 70, 25, 
        hwnd, 
        ID_EDIT, 
        None, 
        None
    )
    # Create static window
    hStatic = win32gui.CreateWindow(
        WC_STATIC, 
        None, 
        win32con.WS_BORDER | win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.SS_LEFT, 
        90, 16, 30, 23, 
        hwnd, 
        ID_STATIC, 
        None, 
        None
    )
    # Set up child window parameters
    win32gui.SendMessage(hUpDown, commctrl.UDM_SETBUDDY, hEdit, 0)
    win32gui.SendMessage(hUpDown, commctrl.UDM_SETRANGE, 0, win32api.MAKELONG(UD_MAX_POS, UD_MIN_POS))
    win32gui.SendMessage(hUpDown, commctrl.UDM_SETPOS, 0, 200)

def main():
    hInstance = win32gui.GetModuleHandle(None)
    wc = win32gui.WNDCLASS()
    wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wc.lpfnWndProc = WndProc
    wc.lpszClassName = "Updown control"
    wc.hInstance = hInstance
    wc.hbrBackground = win32con.COLOR_3DFACE
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(
        wc.lpszClassName, 
        "Updown control", 
        win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE, 
        100, 100, 280, 200, 
        None, 
        None, 
        hInstance, 
        None
    )

    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)
    
    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

