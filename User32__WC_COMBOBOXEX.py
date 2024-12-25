import win32api
import win32gui
import win32con
import commctrl
from ctypes import windll, wintypes, Structure, POINTER, pointer, cast, create_string_buffer, byref, c_int, c_int64, c_bool
# based on nexus-6's c++ code, converted to python code by AI and modified by me

WC_STATIC = "Static"

# Define necessary types
LPCSTR = wintypes.LPCSTR
DWORD = wintypes.DWORD
HFONT = wintypes.HANDLE
HWND = wintypes.HWND
POINT = wintypes.POINT
UINT = wintypes.UINT
# Define the CreateFontA function signature
CreateFont = windll.gdi32.CreateFontA
CreateFont.argtypes = [
    c_int,  # cHeight
    c_int,  # cWidth
    c_int,  # cEscapement
    c_int,  # cOrientation
    c_int,  # cWeight
    DWORD,  # bItalic
    DWORD,  # bUnderline
    DWORD,  # bStrikeOut
    DWORD,  # iCharSet
    DWORD,  # iOutPrecision
    DWORD,  # iClipPrecision
    DWORD,  # iQuality
    DWORD,  # iPitchAndFamily
    LPCSTR  # pszFaceName
]
CreateFont.restype = HFONT

# Define the MapWindowPoints function signature
MapWindowPoints = windll.user32.MapWindowPoints
MapWindowPoints.argtypes = [HWND, HWND, POINTER(POINT), UINT]
MapWindowPoints.restype = c_bool

class COMBOBOXEXITEM(Structure):
    _fields_ = [
        ("mask", wintypes.UINT),
        ("iItem", c_int64),  # Use c_int64 for INT_PTR
        ("pszText", wintypes.LPSTR),
        ("cchTextMax", c_int),
        ("iImage", c_int),
        ("iSelectedImage", c_int),
        ("iOverlay", c_int),
        ("iIndent", c_int),
        ("lParam", wintypes.LPARAM) # Use c_longlong for LPARAM
    ]

# Constants
IDC_COMBOBOXEX = 1
IDC_STATIC_ICON = 2
IDC_STATIC_TEXT = 3

# Global variables
hwndComBoxEx = None
hwndStaticText = None
hwndStaticIcon = None

def WndProc(hwnd, msg, wParam, lParam):
    global hwndComBoxEx, hwndStaticText, hwndStaticIcon
    
    if msg == win32con.WM_CREATE:

        # Create combo box
        hwndComBoxEx = win32gui.CreateWindow(commctrl.WC_COMBOBOXEX, None,
                                                 win32con.WS_BORDER | win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.CBS_DROPDOWN,
                                                 10, 10, 200, 100, hwnd, IDC_COMBOBOXEX, None, None)

        # Create static boxed. One for text the other to display images
        hwndStaticIcon = win32gui.CreateWindow(WC_STATIC, "", 
                                                 win32con.WS_CHILD | win32con.SS_ICON | win32con.WS_VISIBLE,
                                                 230, 15, 40, 40, hwnd, IDC_STATIC_ICON, None, None)

        hwndStaticText = win32gui.CreateWindow(WC_STATIC, "", 
                                                 win32con.WS_CHILD | win32con.WS_VISIBLE,
                                                 270, 15, 150, 40, hwnd, IDC_STATIC_TEXT, None, None)

        # Create custom font
        font = CreateFont(30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"Times New Roman")

        # Set font in both comboboxex and static box
        win32gui.SendMessage(hwndComBoxEx, win32con.WM_SETFONT, font, True)
        win32gui.SendMessage(hwndStaticText, win32con.WM_SETFONT, font, True)

        # Used to set up items in ComboBoxEx control
        cbei = COMBOBOXEXITEM()
        cbei.mask = commctrl.CBEIF_TEXT | commctrl.CBEIF_IMAGE | commctrl.CBEIF_SELECTEDIMAGE

        ITEMINFO = [
            {"pszText": "Chilli", "iImage": 0, "iSelectedImage": 0},
            {"pszText": "Mushroom", "iImage": 1, "iSelectedImage": 1},
            {"pszText": "Onion", "iImage": 2, "iSelectedImage": 2},
            {"pszText": "Pineapple", "iImage": 3, "iSelectedImage": 3},
            {"pszText": "Strawberry", "iImage": 4, "iSelectedImage": 4}
        ]

        # Load BMP images from project folder and insert into image list im_list
        im_list = win32gui.ImageList_Create(32, 32, commctrl.ILC_COLOR | commctrl.ILC_MASK, 4, 0)

        for item in ITEMINFO:
            bitmapicon = win32gui.LoadImage(None, item["pszText"].lower() + ".bmp", win32con.IMAGE_BITMAP, 32, 32, win32con.LR_LOADFROMFILE)
            win32gui.ImageList_Add(im_list, bitmapicon, 0)

        win32gui.SendMessage(hwndComBoxEx, commctrl.CBEM_SETIMAGELIST, 0, im_list)

        # Populate comboboxex with data
        for iCnt in range(5):
            cbei.iItem = iCnt
            cbei.pszText = bytes(ITEMINFO[iCnt]["pszText"].encode("utf-8"))
            cbei.cchTextMax = len(ITEMINFO[iCnt]["pszText"])
            cbei.iImage = ITEMINFO[iCnt]["iImage"]
            cbei.iSelectedImage = ITEMINFO[iCnt]["iSelectedImage"]
            
            # Tell the ComboBoxEx items. Return False if this fails.
            if win32gui.SendMessage(hwndComBoxEx, commctrl.CBEM_INSERTITEM, 0, cbei) == -1:
                return False
    elif msg == win32con.WM_COMMAND:
        # checks combo box clicked
        if lParam == hwndComBoxEx:
            # detects selection change in comboxboxec
            if win32api.HIWORD(wParam) == 5:
                

                # used to obtain selected item data by sending CBEM_GETITEM to ComBoxEx
                buff = create_string_buffer(255)
                info = COMBOBOXEXITEM()
                info.mask = commctrl.CBEIF_TEXT | commctrl.CBEIF_IMAGE | commctrl.CBEIF_SELECTEDIMAGE
                info.iItem = win32gui.SendMessage(hwndComBoxEx, win32con.CB_GETCURSEL, 0, 0)
                info.pszText = cast(pointer(buff), wintypes.LPSTR)
                info.cchTextMax = len(buff)

                win32gui.SendMessage(hwndComBoxEx, commctrl.CBEM_GETITEM, 0, info)

                # get image list from comboboxex and extract selected individual image
                im_list = win32gui.SendMessage(hwndComBoxEx, commctrl.CBEM_GETIMAGELIST, 0, 0)
                im_index = info.iSelectedImage
                selectedicon = win32gui.ImageList_GetIcon(im_list, im_index, win32con.LR_DEFAULTCOLOR)

                # set up static box with selected text and image
                win32gui.SendMessage(hwndStaticIcon, win32con.STM_SETIMAGE, win32con.IMAGE_ICON, selectedicon)
                win32gui.SetWindowText(hwndStaticText, bytes(buff).split(b"\0")[0].decode('utf-8'))

                # redraw static text box after change
                rect = win32gui.GetClientRect(hwndStaticText)
                rect1 = win32gui.GetWindowRect(hwndStaticText)
                win32gui.InvalidateRect(hwndStaticText, rect, True)
                point = POINT(rect[0], rect[1])
                MapWindowPoints(hwndStaticText, hwnd, byref(point), 2)
                rect = (point.x, point.y, rect[2], rect[3])
                #win32gui.RedrawWindow(hwnd, rect, None, win32con.RDW_ERASE | win32con.RDW_INVALIDATE)
                win32gui.RedrawWindow(hwnd, None, None, win32con.RDW_ERASE | win32con.RDW_INVALIDATE)
    elif msg == win32con.WM_CTLCOLORSTATIC:
        if win32gui.GetDlgCtrlID(lParam) in (IDC_STATIC_TEXT, IDC_STATIC_ICON):
            hdc_static = wParam
            win32gui.SetTextColor(hdc_static, win32api.RGB(255, 0, 0))  # set text color
            return win32gui.GetStockObject(win32con.NULL_BRUSH)  # set background to white
    elif msg == win32con.WM_CLOSE:
        win32gui.DestroyWindow(hwnd)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = WndProc
    wc.hInstance = win32api.GetModuleHandle()
    wc.lpszClassName = "myWindowClass"
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
    
    # Register the window class
    win32gui.RegisterClass(wc)
    
    # Create the window
    hwnd = win32gui.CreateWindow(
        wc.lpszClassName,
        "ComboBoxEx Control",
        win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        430,
        200,
        0,
        0,
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

