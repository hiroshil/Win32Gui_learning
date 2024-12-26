import win32gui
import win32con
import win32api
import win32gui_struct
import commctrl
from ctypes import wintypes, Structure, create_string_buffer, cast, c_void_p, c_int
# based on nexus-6's c++ code, converted to python code by AI and modified by me

# Define necessary types
UINT = wintypes.UINT
HTREEITEM = c_void_p
LPWSTR = wintypes.LPWSTR
LPARAM = wintypes.LPARAM

class TVITEM(Structure):
    _fields_ = [
        ("mask", UINT),
        ("hItem", HTREEITEM),
        ("state", UINT),
        ("stateMask", UINT),
        ("pszText", LPWSTR),
        ("cchTextMax", c_int),
        ("iImage", c_int),
        ("iSelectedImage", c_int),
        ("cChildren", c_int),
        ("lParam", LPARAM),
    ]


class TVINSERTSTRUCT(Structure):
    _fields_ = [
        ("hParent", HTREEITEM),
        ("hInsertAfter", HTREEITEM),
        ("item", TVITEM),
    ]

WC_EDIT = "Edit"
WC_BUTTON = "Button"

ID_TREEVIEW = 1
ID_CREATEBUTTON = 2
ID_DELETEBUTTON = 3
ID_EDITBOX = 4

hwndEdit = None
hwndTV = None

def WndProc(hwnd, msg, wParam, lParam):
    global hwndEdit, hwndTV
    if msg == win32con.WM_CREATE:
        # load common control class ICC_LISTVIEW_CLASSES from the dynamic-link library (DLL).
        win32gui.InitCommonControlsEx(commctrl.ICC_LISTVIEW_CLASSES)

        rcClient = win32gui.GetClientRect(hwnd)
        rcClient = wintypes.RECT(*rcClient)

        # Create child windows
        hwndTV = win32gui.CreateWindow(commctrl.WC_TREEVIEW, "Tree View", win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.WS_BORDER | 
                                        commctrl.TVS_HASLINES | commctrl.TVS_LINESATROOT | commctrl.TVS_HASBUTTONS | 
                                        commctrl.TVS_SHOWSELALWAYS, 10, 10, rcClient.right - 50, rcClient.bottom - 50, 
                                        hwnd, ID_TREEVIEW, win32gui.GetWindowLong(hwnd, win32con.GWL_HINSTANCE), None)
        hwndEdit = win32gui.CreateWindow(WC_EDIT, None, win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER, 290, 
                                        rcClient.bottom - 30, 120, 25, hwnd, ID_EDITBOX, win32gui.GetWindowLong(hwnd, win32con.GWL_HINSTANCE), None)  # Edit control
        win32gui.CreateWindow(WC_BUTTON, "Add Child", win32con.WS_CHILD | win32con.WS_VISIBLE, 20, rcClient.bottom - 30, 120, 25, 
                                        hwnd, ID_CREATEBUTTON, win32gui.GetWindowLong(hwnd, win32con.GWL_HINSTANCE), None)
        win32gui.CreateWindow(WC_BUTTON, "Delete Selected", win32con.WS_CHILD | win32con.WS_VISIBLE, 150, rcClient.bottom - 30, 120, 25, 
                                        hwnd, ID_DELETEBUTTON, win32gui.GetWindowLong(hwnd, win32con.GWL_HINSTANCE), None)

        addnode()
    elif msg == win32con.WM_COMMAND:
        # Respond to button click
        if win32gui.HIWORD(wParam) == win32con.BN_CLICKED:
            if win32gui.LOWORD(wParam) == ID_CREATEBUTTON:
                addnode()
            elif win32gui.LOWORD(wParam) == ID_DELETEBUTTON:
                tvIte = win32gui.SendMessage(hwndTV, commctrl.TVM_GETNEXTITEM, commctrl.TVGN_CARET, 0)
                if tvIte:
                    win32gui.SendMessage(hwndTV, commctrl.TVM_DELETEITEM, commctrl.TVGN_CARET, tvIte)
                    win32gui.SetFocus(hwndTV)
    elif msg == win32con.WM_NOTIFY:
        # i'm too lazy to write an unpack function so I picked a random function from the library to use, not recommended to follow
        nmptr = win32gui_struct.UnpackNMITEMACTIVATE(lParam) # NMTREEVIEW
        code = nmptr.code
        if code == commctrl.TVN_SELCHANGED - 48: code += 48
        
        if code == commctrl.NM_DBLCLK:
            # Respond to double click
            print("NM_DBLCLK")
        if code == commctrl.TVN_SELCHANGED:
            # Respond to treeview selection change
            print("TVN_SELCHANGED")
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

# Add node to tree view
def addnode():
    global hwndTV, hwndEdit
    tvinsert = TVINSERTSTRUCT()
    tvinsert.item.mask = commctrl.TVIF_TEXT | commctrl.TVIF_IMAGE | commctrl.TVIF_SELECTEDIMAGE
    totalnodes = win32gui.SendMessage(hwndTV, commctrl.TVM_GETCOUNT, 0, 0)

    # Check if treeview is empty and if so add root node
    if totalnodes == 0:
        tvinsert.hParent = commctrl.TVI_ROOT
        buf = create_string_buffer("root".encode('utf-8'))
        tvinsert.item.pszText = cast(buf, wintypes.LPWSTR)
    else:
        textvalue = win32gui.GetWindowText(hwndEdit)
        stringlength = len(textvalue)
        if stringlength > 0:
            tvIte = win32gui.SendMessage(hwndTV, commctrl.TVM_GETNEXTITEM, commctrl.TVGN_CARET, 0)
            tvinsert.hParent = tvIte
            tvinsert.hInsertAfter = commctrl.TVI_LAST
            buf = create_string_buffer(textvalue.encode('utf-8'))
            tvinsert.item.pszText = cast(buf, wintypes.LPWSTR)

    win32gui.SendMessage(hwndTV, commctrl.TVM_INSERTITEM, 0, bytes(tvinsert))
    win32gui.SetFocus(hwndTV)

def main():
    hInstance = win32gui.GetModuleHandle(None)
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "myWindowClass"
    wc.hInstance = hInstance
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.lpfnWndProc = WndProc
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(wc.lpszClassName, "Treeview control", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE, 10, 10, 550, 200, 0, 0, hInstance, None)

    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)
    
    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

