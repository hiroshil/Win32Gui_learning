import win32gui
import win32con
import win32api
import win32gui_struct
import commctrl
import math
from ctypes import windll, wintypes, Structure, POINTER, create_string_buffer, cast
# data class generated by AI

# Define the GetDeviceCaps function signature
GetDeviceCaps = windll.gdi32.GetDeviceCaps
GetDeviceCaps.argtypes = [wintypes.HDC, wintypes.INT]
GetDeviceCaps.restype = wintypes.INT

class LVCOLUMN(Structure):
    _fields_ = [
        ("mask", wintypes.UINT),
        ("fmt", wintypes.INT),
        ("cx", wintypes.INT),
        ("pszText", wintypes.LPCWSTR),
        ("cchTextMax", wintypes.INT),
        ("iSubItem", wintypes.INT),
        ("iImage", wintypes.INT),
        ("iOrder", wintypes.INT),
        ("cxMin", wintypes.INT),
        ("cxDefault", wintypes.INT),
        ("iGroupId", wintypes.INT)
    ]
class LVITEM(Structure):
    _fields_ = [
        ("mask", wintypes.UINT),
        ("iItem", wintypes.INT),
        ("iSubItem", wintypes.INT),
        ("state", wintypes.UINT),
        ("stateMask", wintypes.UINT),
        ("pszText", wintypes.LPCWSTR),
        ("cchTextMax", wintypes.INT),
        ("iImage", wintypes.INT),
        ("lParam", wintypes.LPARAM),
        ("iIndent", wintypes.INT),
        ("iGroupId", wintypes.INT),
        ("cColumns", wintypes.UINT), # Added for LVIF_COLUMNS
        ("puColumns", POINTER(wintypes.UINT)), # Added for LVIF_COLUMNS
        ("piColFmt", POINTER(wintypes.INT)), # Added for LVIF_COLUMNS
        ("iGroup", wintypes.INT)
    ]
LVM_GETNEXTITEM = (commctrl.LVM_FIRST + 12)

lv_hwnd = int()  # Store the listview handle

def WndProc(hwnd, msg, wParam, lParam):
    global lv_hwnd
    if msg == win32con.WM_COMMAND:
            pass

    elif msg == win32con.WM_NOTIFY:
        # https://github.com/eavatar/eavatar-me/blob/master/src/avashell/win32/console.py#L168
        info = win32gui_struct.UnpackNMITEMACTIVATE(lParam)
        if info.code == commctrl.NM_CLICK:
            # Get selected item index from the listview
            idx = win32gui.SendMessage(lv_hwnd, LVM_GETNEXTITEM, -1, commctrl.LVNI_SELECTED)
            print(f"index of selected item: {idx}")
    
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    dpiX = 0
    dpiY = 0
    hdc = win32gui.GetDC(0)  # 0 represents the entire screen
    if hdc:
        dpiX = GetDeviceCaps(hdc, win32con.LOGPIXELSX)
        dpiY = GetDeviceCaps(hdc, win32con.LOGPIXELSY)
        win32gui.ReleaseDC(0, hdc)

    width = int(math.ceil(640.0 * dpiX / 96.0))
    height = int(math.ceil(480.0 * dpiY / 96.0))
    
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "MyWindowClass"
    wc.lpfnWndProc = WndProc
    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(class_atom, "My Window", win32con.WS_OVERLAPPEDWINDOW,
                                win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, width, height, 0, 0, 0, None)

    # Example listview creation (adjust xpos, ypos, nwidth, nheight, hwndParent)
    xpos, ypos = 10, 10  # Example position
    nwidth, nheight = 430, 200 # Example size
    hwndParent = hwnd # Set parent to the main window
    
    # Create a listbox control
    global lv_hwnd
    lv_hwnd = win32gui.CreateWindow(commctrl.WC_LISTVIEW, "",
                                            win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER | commctrl.LVS_ALIGNLEFT
                                            | commctrl.LVS_REPORT | commctrl.LVS_SHOWSELALWAYS , # Style
                                            xpos, ypos, nwidth, nheight, hwndParent, 101, 0, None)
    # Set default font for List View
    lf = win32gui.LOGFONT()
    lf.lfFaceName = "Calibri"
    lf.lfHeight = 16
    designFont = win32gui.CreateFontIndirect(lf)
    win32gui.SendMessage(lv_hwnd, win32con.WM_SETFONT, designFont, True)
    
    # Set extended styles for List View
    # https://stackoverflow.com/questions/3458914/does-lvs-ex-fullrowselect-have-any-compatibility-issues-with-other-styles
    ex_lv_style = win32gui.SendMessage(lv_hwnd, commctrl.LVM_GETEXTENDEDLISTVIEWSTYLE, 0, 0)
    win32gui.SendMessage(lv_hwnd, commctrl.LVM_SETEXTENDEDLISTVIEWSTYLE,
                            ex_lv_style,
                            commctrl.LVS_EX_FULLROWSELECT | commctrl.LVS_EX_GRIDLINES)
    
    # Insert Column to List View
    szString = ["Column 1", "Column 2", "Column 3"]
    c_cols = 3
    lvc = LVCOLUMN()
    lvc.mask = commctrl.LVCF_FMT | commctrl.LVCF_WIDTH | commctrl.LVCF_TEXT | commctrl.LVCF_SUBITEM
    for iCol in range(c_cols):
        lvc.iSubItem = iCol
        lvc.cx       = int(nwidth/c_cols)        # Width of column in pixels.
        lvc.fmt = commctrl.LVCFMT_LEFT              # Left-aligned column.
        buf = create_string_buffer(szString[iCol].encode('utf-8'))
        lvc.pszText  = cast(buf, wintypes.LPCWSTR)

        win32gui.SendMessage(lv_hwnd, commctrl.LVM_INSERTCOLUMN, iCol, lvc)
    
    # Inserts items into a list view
    c_rows = 8
    lvI = LVITEM()
    
    # Initialize LVITEM members that are common to all items.
    buf = create_string_buffer("item".encode('utf-8'))
    lvI.pszText   = cast(buf, wintypes.LPCWSTR)
    lvI.mask      = commctrl.LVIF_TEXT | commctrl.LVIF_IMAGE | commctrl.LVIF_STATE
    lvI.stateMask = 0
    lvI.state     = 0
    
    # Initialize LVITEM members that are different for each item.
    for i in range(c_rows):
        # https://stackoverflow.com/questions/29990028/add-a-new-row-into-listview
        # First column
        lvI.iItem  = win32gui.SendMessage(lv_hwnd, commctrl.LVM_GETITEMCOUNT, 0, 0)
        lvI.iSubItem  = 0
        index = win32gui.SendMessage(lv_hwnd, commctrl.LVM_INSERTITEM, 0, lvI)
        # Remaining columns
        for j in range(c_cols):
            if index != -1:
                lvI.iItem  = index
                lvI.iImage = j
            
                # Insert items into the list.
                lvI.iSubItem  = j
                win32gui.SendMessage(lv_hwnd, commctrl.LVM_SETITEM, 0, lvI)

    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()