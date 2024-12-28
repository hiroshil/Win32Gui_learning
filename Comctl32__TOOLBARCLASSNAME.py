import win32api
import win32con
import win32gui
import win32gui_struct
import commctrl
import sys
import struct
import array
from ctypes import wintypes, Structure, POINTER, cast, create_string_buffer, memset, sizeof, c_int

is64bit = "64 bit" in sys.version
_nmhdr_fmt = "PPi"
if is64bit:
    # When the item past the NMHDR gets aligned (eg, when it is a struct)
    # we need this many bytes padding.
    _nmhdr_align_padding = "xxxx"
else:
    _nmhdr_align_padding = ""

class TBBUTTON(Structure):
    _fields_ = [
        ("iBitmap", wintypes.INT),
        ("idCommand", wintypes.INT),
        ("fsState", wintypes.BYTE),
        ("fsStyle", wintypes.BYTE),
        ("bReserved", wintypes.BYTE * 6),  # Use the largest size for compatibility
        ("dwData", POINTER(wintypes.DWORD)),
        ("iString", POINTER(wintypes.INT)),
    ]

def UnpackNMPGCALCSIZE(lparam):
    format_str = _nmhdr_fmt + _nmhdr_align_padding
    format_str += "3i"
    buf = win32gui.PyMakeBuffer(struct.calcsize(format_str), lparam)
    return win32gui_struct._MakeResult(
        "NMPGCALCSIZE hwndFrom idFrom code dwFlag iWidth iHeight",
        struct.unpack(format_str, buf),
    )

TB_TEST1 = 1003
TB_TEST2 = 1004
TB_TEST3 = 1005
TB_TEST4 = 1006
TB_TEST5 = 1007
TB_TEST6 = 1008
TB_TEST7 = 1009

hWndToolBar = None
hWndPager = None

def WndProc(hwnd, msg, wParam, lParam):
    global hWndToolBar, hWndPager
    
    if msg == win32con.WM_CREATE:
        win32gui.InitCommonControlsEx(commctrl.ICC_PAGESCROLLER_CLASS)

        # Create toolbar and pager windows
        toolbarBitMap = None  # Placeholder for bitmap
        tbb = (TBBUTTON * 9)()
        imageList = win32gui.ImageList_Create(24, 24, commctrl.ILC_COLOR8 | commctrl.ILC_MASK, 5, 0)

        hWndPager = win32gui.CreateWindow(commctrl.WC_PAGESCROLLER, None, win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.PGS_HORZ, 100, 40, 120, 40, hwnd, None, win32gui.GetModuleHandle(None), None)
        hWndToolBar = win32gui.CreateWindow(commctrl.TOOLBARCLASSNAME, None, commctrl.TBSTYLE_TRANSPARENT | win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.CCS_NORESIZE, 0, 0, 0, 0, hWndPager, None, win32gui.GetModuleHandle(None), None)

        # Add bitmap to image list
        win32gui.ImageList_Add(imageList, toolbarBitMap, None)
        # Add imagelist to toolbar
        win32gui.SendMessage(hWndToolBar, commctrl.TB_SETIMAGELIST, 0, imageList)
        # Add system-defined button image to image list
        win32gui.SendMessage(hWndToolBar, commctrl.TB_LOADIMAGES, commctrl.IDB_STD_LARGE_COLOR, commctrl.HINST_COMMCTRL)

        # Define characteristics of each toolbar button
        for i in range(9):
            tbb[i].iBitmap = i
            tbb[i].idCommand = TB_TEST1 + i  # Placeholder for command IDs
            tbb[i].fsState = commctrl.TBSTATE_ENABLED
            tbb[i].fsStyle = commctrl.TBSTYLE_BUTTON

        # Message TB_ADDBUTTONS add buttons as defined in TBBUTTON structure tbb
        win32gui.SendMessage(hWndToolBar, commctrl.TB_ADDBUTTONS, 9, bytes(tbb))
        # Message TB_AUTOSIZE causes a toolbar to be resized
        win32gui.SendMessage(hWndToolBar, commctrl.TB_AUTOSIZE, 0, 0)
        win32gui.SendMessage(hWndPager, commctrl.PGM_SETCHILD, 0, hWndToolBar)

    elif msg == win32con.WM_NOTIFY:
        hdr = win32gui_struct.UnpackWMNOTIFY(lParam)
        if hdr.code == commctrl.PGN_CALCSIZE:
            pCalcSize = UnpackNMPGCALCSIZE(lParam)
            if pCalcSize.dwFlag == commctrl.PGF_CALCWIDTH:
                size = create_string_buffer(sizeof(wintypes.SIZE))
                win32gui.SendMessage(hWndToolBar, commctrl.TB_GETMAXSIZE, 0, size)
                size = wintypes.SIZE.from_buffer_copy(size)
                # iWidth = size.cx
                iWidth_p = cast(lParam + 28, POINTER(c_int))
                iWidth_p.contents.value = size.cx

    elif msg == win32con.WM_COMMAND:
        if win32gui.LOWORD(wParam) == TB_TEST1:
            # Respond to button clicks
            pass

    elif msg == win32con.WM_CLOSE:
        win32gui.DestroyWindow(hwnd)

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    else:
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

    return 0

def main():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = WndProc
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.lpszClassName = "myWindowClass"
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

    # Register the window class
    win32gui.RegisterClass(wc)

    # Create the window
    hwnd = win32gui.CreateWindow(
        "myWindowClass",
        "Page scroller Demo",
        win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        340,
        150,
        0,
        0,
        win32api.GetModuleHandle(None),
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

