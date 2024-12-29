import win32api
import win32con
import win32gui
import win32gui_struct
import struct
# based on nexus-6's c++ code, converted to python code by AI and modified by me

_ds_fmt = "LLLLLPPllllP"

def UnpackDRAWITEMSTRUCT(lparam):
    ds_size = struct.calcsize(_ds_fmt)
    buf = win32gui.PyGetMemory(lparam, ds_size)
    CtlType, CtlID, itemID, itemAction, itemState, hwndItem, hDC, left, top, right, bottom, itemData = struct.unpack(_ds_fmt, buf)
    rcItem = win32gui_struct._MakeResult("RECT left top right bottom", (left, top, right, bottom),)
    return win32gui_struct._MakeResult(
        "DRAWITEMSTRUCT CtlType CtlID itemID itemAction itemState hwndItem hDC rcItem itemData",
        (CtlType, CtlID, itemID, itemAction, itemState, hwndItem, hDC, rcItem, itemData),
    )

# define constants
IDM_MENUITEM1 = 1001
IDM_MENUITEM2 = 1002
IDM_FILE_QUIT = 1003

def WndProc(hwnd, uMsg, wParam, lParam):
    # The LPMEASUREITEMSTRUCT structure stores the dimensions of an owner-drawn control.
    # The LPDRAWITEMSTRUCT structure stores information required to paint an owner-drawn control
    
    if uMsg == win32con.WM_CREATE:
        # Create menu
        Bar = win32gui.CreateMenu()
        File = win32gui.CreateMenu()
        Edit = win32gui.CreateMenu()
        Help = win32gui.CreateMenu()
        win32gui.AppendMenu(Bar, win32con.MF_POPUP, File, "File")
        win32gui.AppendMenu(Bar, win32con.MF_POPUP, Edit, "Edit")
        # create menu items with ownerdraw attribute
        #win32gui.AppendMenu(File, win32con.MF_OWNERDRAW | win32con.MF_STRING, IDM_MENUITEM2, "Item 1")
        item, extras = win32gui_struct.PackMENUITEMINFO(fType=win32con.MFT_OWNERDRAW, text="Item 1", 
                                                        wID = IDM_MENUITEM1)
        win32gui.InsertMenuItem(File, 0, True, item)
        #win32gui.AppendMenu(File, win32con.MF_OWNERDRAW | win32con.MF_STRING, IDM_MENUITEM1, "Item 2")
        item, extras = win32gui_struct.PackMENUITEMINFO(fType=win32con.MFT_OWNERDRAW, text="Item 2", 
                                                        wID = IDM_MENUITEM2)
        win32gui.InsertMenuItem(File, 1, True, item)
        win32gui.AppendMenu(Edit, win32con.MF_STRING, IDM_FILE_QUIT, "Quit")
        win32gui.SetMenu(hwnd, Bar)

    elif uMsg == win32con.WM_MEASUREITEM:
        buf = win32gui.PyGetMemory(lParam + struct.calcsize(_ds_fmt[:2]), struct.calcsize(_ds_fmt[3]))
        itemID = struct.unpack(_ds_fmt[3], buf)[0]
        # set width and height of first and second drop down menu item
        if itemID == IDM_MENUITEM1:
            win32gui.PySetMemory(lParam + struct.calcsize(_ds_fmt[:3]), struct.pack(_ds_fmt[4], 120))
            win32gui.PySetMemory(lParam + struct.calcsize(_ds_fmt[:4]), struct.pack(_ds_fmt[5], 70))
        if itemID == IDM_MENUITEM2:
            win32gui.PySetMemory(lParam + struct.calcsize(_ds_fmt[:3]), struct.pack(_ds_fmt[4], 120))
            win32gui.PySetMemory(lParam + struct.calcsize(_ds_fmt[:4]), struct.pack(_ds_fmt[5], 50))
        return True  # Important to return True

    elif uMsg == win32con.WM_DRAWITEM:
        dis = UnpackDRAWITEMSTRUCT(lParam)
        # detects if the selection status of the menu item has changed. If so draw bounding box and change text colour
        if dis.itemState & win32con.ODS_SELECTED:
            win32gui.SetTextColor(dis.hDC, win32api.RGB(255, 55, 55))
            bkBrush = win32gui.CreateSolidBrush(win32api.RGB(0, 0, 0))
            win32gui.FillRect(dis.hDC, dis.rcItem, bkBrush)
        else:
            win32gui.SetTextColor(dis.hDC, win32api.RGB(0, 0, 0))
            bkBrush = win32gui.CreateSolidBrush(win32api.RGB(255, 255, 255))
            win32gui.FillRect(dis.hDC, dis.rcItem, bkBrush)
        
        #set menu item text and appearance
        bkBrush = win32gui.CreateSolidBrush(win32api.RGB(255,255,0))
        oldBrush = win32gui.SelectObject(dis.hDC, bkBrush)
        win32gui.SetBkColor(dis.hDC,win32api.RGB(255,255,0))
        rect = dis.rcItem
        rect = (rect[0] + 5, rect[1] + 3, rect[2], rect[3])
        win32gui.Rectangle(dis.hDC, dis.rcItem[0] + 2, dis.rcItem[1] + 2, dis.rcItem[2] - 2, dis.rcItem[3] - 2)
        buf, extras = win32gui_struct.EmptyMENUITEMINFO()
        win32gui.GetMenuItemInfo(dis.hwndItem, dis.itemID, False, buf)
        item = win32gui_struct.UnpackMENUITEMINFO(buf)
        win32gui.DrawText(dis.hDC, item.text, -1, tuple(rect), win32con.DT_SINGLELINE | win32con.DT_INTERNAL)
        win32gui.SelectObject(dis.hDC, oldBrush)
        
        if (dis.itemID==IDM_MENUITEM1):
            pass # used to set specific draw attributes for menu item 1
        if (dis.itemID==IDM_MENUITEM2):
            pass # used to set specific draw attributes for menu item 2
        
        win32gui.DeleteObject(bkBrush)
        return True # Important to return True

    elif uMsg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    else:
        return win32gui.DefWindowProc(hwnd, uMsg, wParam, lParam)

    return 0

# Main function (similar to wWinMain)
wc = win32gui.WNDCLASS()
wc.lpszClassName = "Menu Demonstration"
wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW #Added styles
wc.lpfnWndProc = WndProc
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)


hInstance = win32api.GetModuleHandle(None)
win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(wc.lpszClassName, "Owner drawn menu", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE, 100, 100, 350, 180, 0, 0, hInstance, None)

win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32

# Dispatch messages
win32gui.PumpMessages()