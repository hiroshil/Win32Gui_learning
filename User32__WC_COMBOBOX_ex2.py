import win32api
import win32con
import win32gui
from win32gui_struct import _make_empty_text_buffer
# based on nexus-6's c++ code, converted to python code by AI and modified by me

WC_COMBOBOX = "ComboBox"
WC_STATIC = "Static"

def WndProc(hwnd, msg, wParam, lParam):

    if msg == win32con.WM_COMMAND:
        # respond to combo box selection
        if win32api.HIWORD(wParam) == win32con.CBN_SELCHANGE:

            # get position of selected item
            sel = win32gui.SendMessage(hwndCombo, win32con.CB_GETCURSEL, 0, 0)
            
            # get selected item text
            # https://github.com/smontanaro/spambayes/blob/master/spambayes/Outlook2000/dialogs/opt_processors.py#L162
            txtLen = win32gui.SendMessage(hwndCombo, win32con.CB_GETLBTEXTLEN, sel)
            strText = _make_empty_text_buffer(txtLen+1)
            win32gui.SendMessage(hwndCombo, win32con.CB_GETLBTEXT, sel, strText)
            
            # set value of static bex to value selected in combo box
            win32gui.SetWindowText(hwndStatic, strText.tobytes().decode('utf-16le'))
            win32gui.SetFocus(hwnd)

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        
    # return DefWindowProc(hwnd, msg, wParam, lParam);
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
    "Combobox control demo",
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

items = ["Paris", "London", "Berlin", "Rome"]

# create combo box
hwndCombo = win32gui.CreateWindow(
    WC_COMBOBOX,
    None,
    win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.CBS_DROPDOWN,
    10, 10, 120, 110,
    hwnd,
    None,
    None,
    None
)

# create static control
hwndStatic = win32gui.CreateWindow(
    WC_STATIC,
    "",
    win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER,
    150, 10, 90, 25,
    hwnd,
    None,
    None,
    None
)

for i in range(len(items)):
    # populate combo box
    win32gui.SendMessage(hwndCombo, win32con.CB_ADDSTRING, 0, items[i])

# Show & update the window
win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
win32gui.UpdateWindow(hwnd)

# Dispatch messages
win32gui.PumpMessages()