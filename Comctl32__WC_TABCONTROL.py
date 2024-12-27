import win32api
import win32con
import win32gui
import win32gui_struct
import commctrl
from ctypes import wintypes, Structure, c_int
# based on nexus-6's c++ code, converted to python code by AI and modified by me

class TCITEM(Structure):
    _fields_ = [
        ("mask", wintypes.UINT),
        ("dwState", wintypes.DWORD),
        ("dwStateMask", wintypes.DWORD),
        ("pszText", wintypes.LPSTR),
        ("cchTextMax", c_int),
        ("iImage", c_int),
        ("lParam", wintypes.LPARAM),
    ]

# Constants
WC_EDIT = "Edit"
WC_BUTTON = "Button"
TCN_SELCHANGE = (commctrl.TCN_FIRST - 1)
TCN_SELCHANGING = (commctrl.TCN_FIRST - 2)
TCN_GETOBJECT = (commctrl.TCN_FIRST - 3)
TCN_FOCUSCHANGE = (commctrl.TCN_FIRST - 4)

ID_TABCTRL = 1
ID_EDIT = 2
BTN_ADD = 3
BTN_DEL = 4
BTN_CLR = 5
MAX_TAB_LEN = 15

hTab = None
hEdit = None

def WndProc(hwnd, msg, wParam, lParam):
    global hTab, hEdit

    if msg == win32con.WM_CREATE:
        # Load common control class ICC_TAB_CLASSES
        win32gui.InitCommonControlsEx(commctrl.ICC_TAB_CLASSES)
        
        # Create tab control
        hTab = win32gui.CreateWindow(commctrl.WC_TABCONTROL, None,
                                       win32con.WS_CHILD | win32con.WS_VISIBLE,
                                       10, 10, 200, 150, hwnd, ID_TABCTRL, 0, None)
        
        hEdit = win32gui.CreateWindow(WC_EDIT, None,
                                       win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER,
                                       250, 20, 100, 25, hwnd, ID_EDIT, 0, None)
        win32gui.SendMessage(hEdit, win32con.EM_SETLIMITTEXT, MAX_TAB_LEN, 0)

        win32gui.CreateWindow(WC_BUTTON, "Add", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_PUSHBUTTON,
                                250, 50, 100, 25, hwnd, BTN_ADD, 0, None)
        win32gui.CreateWindow(WC_BUTTON, "Delete", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_PUSHBUTTON,
                                250, 80, 100, 25, hwnd, BTN_DEL, 0, None)
        win32gui.CreateWindow(WC_BUTTON, "Clear", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_PUSHBUTTON,
                                250, 110, 100, 25, hwnd, BTN_CLR, 0, None)

    elif msg == win32con.WM_COMMAND:
        if win32api.LOWORD(wParam) == BTN_ADD:
          text = win32gui.GetWindowText(hEdit)
          if len(text) != 0:
            tbinfo = TCITEM()
            tbinfo.mask = commctrl.TCIF_TEXT
            tbinfo.pszText = bytes(text.encode("utf-8"))
            count = win32gui.SendMessage(hTab, commctrl.TCM_GETITEMCOUNT, 0, 0)
            win32gui.SendMessage(hTab, commctrl.TCM_INSERTITEM, count, bytes(tbinfo))

        elif win32api.LOWORD(wParam) == BTN_DEL:
          h_id = win32gui.SendMessage(hTab, commctrl.TCM_GETCURSEL, 0, 0)
          if h_id != -1:
            win32gui.SendMessage(hTab, commctrl.TCM_DELETEITEM, 0, h_id)
        elif win32api.LOWORD(wParam) == BTN_CLR:
          win32gui.SendMessage(hTab, commctrl.TCM_DELETEALLITEMS, 0, 0)

    elif msg == win32con.WM_NOTIFY:
    # detects change in data time control
        lpTabselect = win32gui_struct.UnpackWMNOTIFY(lParam)
        if lpTabselect.code == TCN_SELCHANGE or lpTabselect.code == TCN_SELCHANGING:
            pass #handle tab change
        
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)


def main():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "Tab control"
    wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
    wc.lpfnWndProc = WndProc
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    hinst = win32api.GetModuleHandle(None)
    win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(wc.lpszClassName, "Tab control",
                               win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                               100, 100, 380, 230, 0, 0, hinst, None)

    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    # Update the window
    win32gui.UpdateWindow(hwnd)
    
    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == '__main__':
    main()