import win32api
import win32con
import win32gui
import commctrl
import win32gui_struct
from ctypes import wintypes, Structure, POINTER, pointer, c_int, c_void_p
# based on nexus-6's c++ code, converted to python code by AI and modified by me


# Define the WINDOWPOS structure
class WINDOWPOS(Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("hwndInsertAfter", wintypes.HWND),
        ("x", c_int),
        ("y", c_int),
        ("cx", c_int),
        ("cy", c_int),
        ("flags", wintypes.UINT),
    ]

# Define the HDLAYOUT structure
class HDLAYOUT(Structure):
    _fields_ = [
        ("prc", POINTER(wintypes.RECT)),
        ("pwpos", POINTER(WINDOWPOS)),
    ]

class HDITEM(Structure):
    _fields_ = [
        ("mask", wintypes.UINT),
        ("cxy", c_int),
        ("pszText", wintypes.LPSTR),
        ("hbm", wintypes.HBITMAP),
        ("cchTextMax", c_int),
        ("fmt", c_int),
        ("lParam", wintypes.LPARAM),
        ("iImage", c_int),
        ("iOrder", c_int),
        ("type", wintypes.UINT),
        ("pvFilter", c_void_p),
        ("state", wintypes.UINT),
    ]

ID_HEADER = 100
header_ctl = None

def create_header(hwnd_parent):
    hwnd_header = win32gui.CreateWindow(
        commctrl.WC_HEADER,
        None,
        win32con.WS_CHILD | win32con.WS_BORDER | commctrl.HDS_BUTTONS | commctrl.HDS_HORZ,
        0, 0, 0, 0,
        hwnd_parent,
        ID_HEADER,
        win32api.GetModuleHandle(None),
        None
    )
    if hwnd_header is None:
        return None

    rc_parent = win32gui.GetClientRect(hwnd_parent)
    # https://stackoverflow.com/questions/1825715/how-to-pack-and-unpack-using-ctypes-structure-str
    rect = wintypes.RECT(*rc_parent)
    wp = WINDOWPOS()
    hdl = HDLAYOUT(pointer(rect), pointer(wp))
    
    if not win32gui.SendMessage(hwnd_header, commctrl.HDM_LAYOUT, 0, bytes(hdl)):
        return None

    # Set the size, position, and appearance of the header control. 
    win32gui.SetWindowPos(hwnd_header, wp.hwndInsertAfter, wp.x, wp.y, wp.cx, wp.cy, wp.flags | win32con.SWP_SHOWWINDOW)

    hdi = HDITEM()
    hdi.mask = commctrl.HDI_TEXT | commctrl.HDI_FORMAT | commctrl.HDI_WIDTH
    hdi.pszText = b"column 1"
    hdi.cxy = 150
    hdi.cchTextMax = len(hdi.pszText)
    hdi.fmt = commctrl.HDF_LEFT | commctrl.HDF_STRING
    win32gui.SendMessage(hwnd_header, commctrl.HDM_INSERTITEM, 0, bytes(hdi))

    hdi.pszText = b"column 2"
    hdi.cxy = rc_parent[2] - 150
    hdi.cchTextMax = len(hdi.pszText)
    win32gui.SendMessage(hwnd_header, commctrl.HDM_INSERTITEM, 1, bytes(hdi))

    return hwnd_header

def wnd_proc(hwnd, msg, w_param, l_param):
    global header_ctl
    if msg == win32con.WM_CREATE:
        # load common control class ICC_LISTVIEW_CLASSES from the dynamic-link library (DLL)
        #init_common_controls()
        header_ctl = create_header(hwnd)
    # respond to windows size change.
    elif msg == win32con.WM_SIZE:
        rect = win32gui.GetClientRect(hwnd)
        wrect = wintypes.RECT(*rect)
        winpos = WINDOWPOS()
        hdl = HDLAYOUT(pointer(wrect), pointer(winpos))
        win32gui.SendMessage(header_ctl, commctrl.HDM_LAYOUT, 0, bytes(hdl)) # align first header
        win32gui.MoveWindow(header_ctl, winpos.x, winpos.y, winpos.cx, winpos.cy, True)
        
        hdi = HDITEM()
        hdi.mask = commctrl.HDI_TEXT | commctrl.HDI_FORMAT | commctrl.HDI_WIDTH
        hdi.pszText = b"column 2"
        hdi.cxy = rect[2]
        hdi.cchTextMax = len(hdi.pszText)
        hdi.fmt = commctrl.HDF_LEFT | commctrl.HDF_STRING
        win32gui.SendMessage(header_ctl, commctrl.HDM_SETITEM, 1, bytes(hdi)) # align second header
    # detects change in header control
    elif msg == win32con.WM_NOTIFY:
        # i'm too lazy to write an unpack function so I picked a random function from the library to use, not recommended to follow
        header_item = win32gui_struct.UnpackNMITEMACTIVATE(l_param)
        header_item = header_item._replace(code = header_item.code + 20)
        # respond to header click and display message boz
        if header_item.code == commctrl.HDN_ITEMCLICK:
            if header_item.iItem == 0:
                win32gui.MessageBox(None, "header 1", "header 1 clicked", win32con.MB_OK)
            elif header_item.iItem == 1:
                win32gui.MessageBox(None, "header 2", "header 2 clicked", win32con.MB_OK)
    elif msg == win32con.WM_CLOSE:
        win32gui.DestroyWindow(hwnd)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    else:
        return win32gui.DefWindowProc(hwnd, msg, w_param, l_param)
    return 0

def main():
    wc = win32gui.WNDCLASS()
    wc.style = 0
    wc.lpfnWndProc = wnd_proc
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hIcon = win32gui.LoadIcon(None, win32con.IDI_APPLICATION)
    wc.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.lpszClassName = "myWindowClass"

    win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(
        "myWindowClass",
        "Header Control",
        win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        400,
        120,
        None,
        None,
        wc.hInstance,
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

