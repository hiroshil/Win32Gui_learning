import win32api
import win32con
import win32gui
import win32ui
from win32gui_struct import _make_empty_text_buffer, _MakeResult
import struct
from ctypes import wintypes, POINTER, cast, sizeof
# based on nexus-6's c++ code, converted to python code by AI and modified by me

_ds_fmt = "LLLLLPPllllP"

def UnpackDRAWITEMSTRUCT(lparam):
    ds_size = struct.calcsize(_ds_fmt)
    buf = win32gui.PyGetMemory(lparam, ds_size)
    CtlType, CtlID, itemID, itemAction, itemState, hwndItem, hDC, left, top, right, bottom, itemData = struct.unpack(_ds_fmt, buf)
    rcItem = _MakeResult("RECT left top right bottom", (left, top, right, bottom),)
    return _MakeResult(
        "DRAWITEMSTRUCT CtlType CtlID itemID itemAction itemState hwndItem hDC rcItem itemData",
        (CtlType, CtlID, itemID, itemAction, itemState, hwndItem, hDC, rcItem, itemData),
    )

WC_LISTBOX = "ListBox"
WC_STATIC = "Static"

# Define control IDs
IDC_LIST = 1
IDC_STATIC = 2
LBTEXTSIZE = 20

# Global variables for window handles
hwndListBox = None
hwndStatic = None

# Placeholder for bitmaps (replace with actual image loading)
hbmpPicture = None
hbmOld = None

# draw customised listbox
def ListBoxDraw(hwnd, uCtrlId, dis):
    """
    Custom drawing function for the listbox.
    """
    global hbmpPicture, hbmOld
    
    try:    
      # Example
        lbText = _make_empty_text_buffer(LBTEXTSIZE)
        if dis.itemAction in (win32con.ODA_SELECT, win32con.ODA_DRAWENTIRE):
            # Set selected item state
            if dis.itemState & win32con.ODS_SELECTED:
                win32gui.SetTextColor(dis.hDC, win32gui.GetSysColor(win32con.COLOR_HIGHLIGHTTEXT))
                win32gui.SetBkColor(dis.hDC, win32gui.GetSysColor(win32con.COLOR_HIGHLIGHT))
            else:
                win32gui.SetTextColor(dis.hDC, win32gui.GetSysColor(win32con.COLOR_WINDOWTEXT))
                win32gui.SetBkColor(dis.hDC, win32gui.GetSysColor(win32con.COLOR_WINDOW))

            # Set listbox characteristics including font
            hdcMem = win32gui.CreateCompatibleDC(dis.hDC)
            #font = CreateFont(30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"Arial") # Changed font name to "Arial"
            lf = win32gui.LOGFONT()
            lf.lfFaceName = "Arial"
            lf.lfHeight = 30
            font = win32gui.CreateFontIndirect(lf)

            # tm = win32gui.GetTextMetrics(dis.hDC);
            win32gui.SelectObject(dis.hDC, font)

            # Set listbox contents
            win32gui.SendMessage(hwndListBox, win32con.LB_GETTEXT, dis.itemID, lbText)
            hbmpPicture = win32gui.SendMessage(dis.hwndItem, win32con.LB_GETITEMDATA, dis.itemID, 0)
            win32gui.ExtTextOut(dis.hDC, 80, dis.rcItem.top + 20, win32con.ETO_OPAQUE, dis.rcItem, bytes(lbText).decode("utf-16le"), None)

            hbmOld = win32gui.SelectObject(hdcMem, hbmpPicture)
            win32gui.BitBlt(dis.hDC, dis.rcItem.left +10, dis.rcItem.top + 20, dis.rcItem.right - dis.rcItem.left, dis.rcItem.bottom - dis.rcItem.top, hdcMem, 0, 0, win32con.SRCAND)
            win32gui.DeleteDC(hdcMem)
            win32gui.DeleteObject(font)
            hbmpPicture = None
        return True
    except Exception as e:
        print(f"Error in ListBoxDraw: {e}")
        return False

def StaticDraw(hwnd, uCtrlId, dis):
    global hbmpPicture, hbmOld
    
    hInstance = win32api.GetModuleHandle(None)
    lbText = '' # Initialize lbText

    # try:
      # length = win32gui.SendMessage(hwndStatic, win32con.WM_GETTEXTLENGTH)*2
      # buffer = win32gui.PyMakeBuffer(length) # Use a buffer for text
    # except Exception as e:
        # print(f"Error creating buffer: {e}")
        # return False # Handle error appropriately


    if dis.itemAction in (win32con.ODA_SELECT, win32con.ODA_DRAWENTIRE):
        # set static box font
        #font = CreateFont(30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"Ariel")  # Ariel -> "Arial"
        lf = win32gui.LOGFONT()
        lf.lfFaceName = "Arial"
        lf.lfHeight = 30
        font = win32gui.CreateFontIndirect(lf)

        win32gui.SelectObject(dis.hDC, font)
        
        # set static box content
        # hwndListBox = win32gui.GetDlgItem(hwnd, uCtrlId) #get the listbox handle
        sel = win32gui.SendMessage(hwndListBox, win32con.LB_GETCURSEL, 0, 0)
        try:
          hbmpPicture = win32gui.SendMessage(hwndListBox, win32con.LB_GETITEMDATA, sel, 0)
          hdcMem = win32gui.CreateCompatibleDC(dis.hDC)
          hbmOld = win32gui.SelectObject(hdcMem, hbmpPicture)
        except Exception as e:
            print(f"Error getting bitmap: {e}")
            win32gui.DeleteObject(font) #cleanup font
            return False
          
        # hwndStatic = win32gui.GetDlgItem(hwnd, uCtrlId) # Replace with actual Static control ID
        try:
          #win32gui.SendMessage(hwndStatic, win32con.WM_GETTEXT, length, buffer)
          lbText = win32gui.GetWindowText(hwndStatic)
        except Exception as e:
          print(f"Error getting static control text: {e}")
          win32gui.DeleteObject(font)
          win32gui.DeleteDC(hdcMem)
          return False # Handle error

        #address, length_ = win32gui.PyGetBufferAddressAndLen(buffer[:-1])
        #lbText = win32gui.PyGetString(address, length_) #[:int(length/2)]
        win32gui.ExtTextOut(dis.hDC, 75, 20, win32con.ETO_OPAQUE, dis.rcItem, lbText, None)

        try:
            win32gui.BitBlt(dis.hDC, dis.rcItem.left +10, dis.rcItem.top + 20, dis.rcItem.right - dis.rcItem.left, dis.rcItem.bottom - dis.rcItem.top, hdcMem, 0, 0, win32con.SRCAND)
        except Exception as e:
            print(f"Error in BitBlt: {e}")

        win32gui.DeleteObject(font)
        win32gui.DeleteDC(hdcMem)

    return True
    
def WndProc(hwnd, msg, wParam, lParam):
    """
    Window procedure for handling window messages.
    """
    global hwndListBox, hwndStatic, hbmpPicture
    
    try:
        if msg == win32con.WM_CREATE:
            hInstance = win32api.GetModuleHandle(None)

            # create customised listbox by using using LB_OWNERDRAWFIXED flag
            hwndListBox = win32gui.CreateWindow(
                WC_LISTBOX,
                "",
                win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.LBS_OWNERDRAWFIXED | win32con.LBS_OWNERDRAWVARIABLE | win32con.LBS_HASSTRINGS | win32con.LBS_NOTIFY | win32con.WS_BORDER | win32con.WS_VSCROLL,
                10, 10, 300, 240,
                hwnd,
                IDC_LIST,
                hInstance,
                None
            )

            # create customised static box by using using SS_OWNERDRAW flag
            hwndStatic = win32gui.CreateWindow(
                WC_STATIC,
                "",
                win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.SS_OWNERDRAW | win32con.WS_BORDER,
                330, 10, 250, 70,
                hwnd,
                IDC_STATIC,
                hInstance,
                None
            )

            # Populate listbox
            items = ["chilli", "mushroom", "onion", "pineapple", "strawberry"]
            for item in items:
                win32gui.SendMessage(hwndListBox, win32con.LB_ADDSTRING, 0, item)

            # Add images to listbox (replace with your actual bitmap loading)
            try:
                for i, item in enumerate(items):
                    hbmpPicture = win32gui.LoadImage(None, item.lower() + ".bmp", win32con.IMAGE_BITMAP, 32, 32, win32con.LR_LOADFROMFILE)
                    #win32gui.LoadBitmap(hInstance, win32api.MAKEINTRESOURCE(IDB_BITMAP1))
                    win32gui.SendMessage(hwndListBox, win32con.LB_SETITEMDATA, i, hbmpPicture)
            except Exception as e:
                print(f"Error loading bitmaps: {e}") # Handle bitmap loading errors

        elif msg == win32con.WM_COMMAND:
            # Responds to selection change
            if win32api.HIWORD(wParam) == win32con.LBN_SELCHANGE:
                hwndCombo = win32gui.GetDlgItem(hwnd, IDC_LIST)
                value = _make_empty_text_buffer(LBTEXTSIZE)  # Initialize with null characters
                sel = win32gui.SendMessage(hwndCombo, win32con.LB_GETCURSEL, 0, 0)
                
                # Assuming hbmpPicture is a global variable or member of a class
                hbmpPicture = win32gui.SendMessage(hwndCombo, win32con.LB_GETITEMDATA, sel, 0)
                
                # SendMessage parameters modified as per pywin32 documentation
                win32gui.SendMessage(hwndCombo, win32con.LB_GETTEXT, sel, value)
                
                #hwndStatic = win32gui.GetDlgItem(hwnd, IDC_STATIC)
                win32gui.SendMessage(hwndStatic, win32con.WM_SETTEXT, 0, value)  # Set the static control text

        # The WM_DRAWITEM message is sent to the parent window of an owner-drawn button when a visual aspect of that control has been changed.
        elif msg == win32con.WM_DRAWITEM:
            if wParam == IDC_LIST:  # for listbox
                ListBoxDraw(hwnd, wParam, UnpackDRAWITEMSTRUCT(lParam))
            elif wParam == IDC_STATIC:  # for button
                StaticDraw(hwnd, wParam, UnpackDRAWITEMSTRUCT(lParam))

        # WM_MEASUREITEM send to the owner window of a control when the control is created.
        elif msg == win32con.WM_MEASUREITEM:
            lp_itemHeight = cast(lParam + (4*sizeof(wintypes.UINT)), POINTER(wintypes.UINT))  # PMEASUREITEMSTRUCT->itemHeight
            lp_itemHeight.contents.value = 60 # contains the item height of the owner-drawn listview item. 

            return True  # return True for WM_MEASUREITEM

        elif msg == win32con.WM_DESTROY:
            try: 
                win32gui.DeleteObject(hbmpPicture)
            except: pass
            try: 
                win32gui.DeleteObject(hbmOld)
            except: pass
            win32gui.PostQuitMessage(0)
            return 0

        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
    except Exception as e:
        print(f"Error in WndProc: {e}")  # Add error handling
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    # Register window class
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = WndProc
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.lpszClassName = "myWindowClass"

    win32gui.RegisterClass(wc)

    # Create window
    hwnd = win32gui.CreateWindow(
        "myWindowClass",
        "Owner-Drawn Control",
        win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
        win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 660, 300,
        0, 0, win32api.GetModuleHandle(None), None
    )

    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    # Message loop
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()