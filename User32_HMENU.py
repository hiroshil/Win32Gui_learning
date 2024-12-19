import win32api
import win32con
import win32gui
import win32gui_struct
# based on nexus-6's c++ code, converted to python code by AI and modified by me

def LOWORD(dword): return dword & 0x0000ffff
def HIWORD(dword): return dword >> 16

IDM_MENUITEM1 = 1
IDM_MENUITEM2 = 2
IDM_FILE_QUIT = 3

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_COMMAND:
        if LOWORD(wParam) == IDM_MENUITEM1:
            win32api.MessageBeep(win32con.MB_ICONINFORMATION)
        elif LOWORD(wParam) == IDM_MENUITEM2:
            win32api.MessageBeep(win32con.MB_ICONWARNING)
        elif LOWORD(wParam) == IDM_FILE_QUIT:
            win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    
    elif msg == win32con.WM_INITMENU:
        selectedMenuID = wParam  # menu ID of selected menu item
    
    elif msg == win32con.WM_MENUSELECT:
        # with wParam win32api.LOWORD use Python int too large to convert to C long
        uItem = LOWORD(wParam)  # menu item or submenu index
        muFlags = HIWORD(wParam)  # menu flags
        hmenu = lParam  # handle of menu clicked
    
    elif msg == win32con.WM_INITMENUPOPUP:
        hMenuPopup = wParam  # handle of submenu
        uPos = LOWORD(lParam)  # submenu item position
        bSystemMenu = HIWORD(lParam)  # window menu flag
    
    elif msg == win32con.WM_RBUTTONUP:
        point = (LOWORD(lParam), HIWORD(lParam))
        hContextMenu = win32gui.CreatePopupMenu()
        
        # Convert client coordinates to screen coordinates
        win32gui.ClientToScreen(hwnd, point)
        
        # Add menu items to context menu
        win32gui.AppendMenu(hContextMenu, win32con.MF_STRING, IDM_MENUITEM1, "Option1")
        win32gui.AppendMenu(hContextMenu, win32con.MF_STRING, IDM_MENUITEM2, "Option2")
        win32gui.AppendMenu(hContextMenu, win32con.MF_SEPARATOR, 0, '')
        win32gui.AppendMenu(hContextMenu, win32con.MF_STRING, IDM_FILE_QUIT, "Quit")
        
        # Displays popup menu
        # fix TrackPopupMenu position wrong in pywin32
        menu_pos = win32gui.GetMenuItemRect(hwnd, hContextMenu, 0)[1]
        win32gui.TrackPopupMenu(hContextMenu, win32con.TPM_RIGHTBUTTON, menu_pos[0] + point[0], menu_pos[1] + point[1], 0, hwnd, None)
        win32gui.DestroyMenu(hContextMenu)
    
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

wc = win32gui.WNDCLASS()
wc.style = 0
wc.lpfnWndProc = WndProc
wc.hInstance = win32api.GetModuleHandle()
wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32con.COLOR_WINDOW + 1
wc.lpszClassName = "myWindowClass"

class_atom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(
    class_atom,
    "Creating Menus",
    win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
    win32con.CW_USEDEFAULT,
    win32con.CW_USEDEFAULT,
    700,
    200,
    0,
    0,
    win32api.GetModuleHandle(),
    None
)

# Create handles for different types of menu
hMenubar = win32gui.CreateMenu()
hMenu = win32gui.CreateMenu()

# Create top level popup menu
win32gui.AppendMenu(hMenubar, win32con.MF_POPUP, hMenu, "&File")

# Add menu items to pop up window
win32gui.AppendMenu(hMenu, win32con.MF_STRING, IDM_MENUITEM1, "Item1")
win32gui.AppendMenu(hMenu, win32con.MF_STRING, IDM_MENUITEM2, "Item2")
win32gui.AppendMenu(hMenu, win32con.MF_SEPARATOR, 0, '')
win32gui.AppendMenu(hMenu, win32con.MF_STRING, IDM_FILE_QUIT, "Quit")

# Assigns a new menu to the specified window.
win32gui.SetMenu(hwnd, hMenubar)

# Show & update the window
win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
win32gui.UpdateWindow(hwnd)

# Dispatch messages
win32gui.PumpMessages()