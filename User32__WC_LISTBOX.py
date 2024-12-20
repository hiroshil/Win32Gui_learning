import win32api
import win32con
import win32gui
from win32gui_struct import _make_empty_text_buffer
# based on nexus-6's c++ code, converted to python code by AI and modified by me

WC_LISTBOX = "ListBox"

IDC_LIST = 1
ID_EDIT = 2

def WndProc(hwnd, msg, wParam, lParam):
    
    if msg == win32con.WM_COMMAND:
        # respond to listview click
        if win32api.LOWORD(wParam) == IDC_LIST:
            if win32api.HIWORD(wParam) == win32con.LBN_SELCHANGE:
                lbvalue = _make_empty_text_buffer(30)
                # gets index of selected listview item
                sel = win32gui.SendMessage(static_hwnd_list, win32con.LB_GETCURSEL, 0, 0)
                # get selected text
                win32gui.SendMessage(static_hwnd_list, win32con.LB_GETTEXT, sel, lbvalue)
                # sets staticbox to value of listbox text
                win32gui.SendMessage(static_hwnd_static, win32con.WM_SETTEXT, sel, lbvalue)
    
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

wc = win32gui.WNDCLASS()
wc.style = 0
wc.lpfnWndProc = WndProc
wc.hInstance = win32gui.GetModuleHandle(None)
wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32con.COLOR_WINDOW + 1
wc.lpszClassName = "myWindowClass"

class_atom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(
    class_atom,
    "Listbox Demo",
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

names = ["Matthew", "Mark", "Luke", "John"]

# create listbox
static_hwnd_list = win32gui.CreateWindow(
    "ListBox", "", 
    win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.LBS_NOTIFY | win32con.WS_BORDER | win32con.WS_VSCROLL, 
    10, 10, 150, 80, hwnd, 
    IDC_LIST, None, None
)
# create staticbox
static_hwnd_static = win32gui.CreateWindow(
    "static", None, 
    win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER, 
    10, 90, 150, 25, hwnd, 
    ID_EDIT, None, None
)
# populates listbox
for i in range(4):
    win32gui.SendMessage(static_hwnd_list, win32con.LB_ADDSTRING, 0, names[i])

# Show & update the window
win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
win32gui.UpdateWindow(hwnd)

# Dispatch messages
win32gui.PumpMessages()