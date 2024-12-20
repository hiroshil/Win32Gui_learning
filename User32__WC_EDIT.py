import win32gui
import win32api
import win32con
# based on nexus-6's c++ code, converted to python code by AI

WC_EDIT = "Edit"
WC_STATIC = "Static"
WC_BUTTON = "Button"
ID_EDIT = 1
ID_BUTTON = 2

hwndEdit = None
hwndButton = None
hwndStatic = None

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_COMMAND:
        # responds to button click
        if win32api.HIWORD(wParam) == win32con.BN_CLICKED:
            maxtextlength = 30
            textvalue = win32gui.GetWindowText(hwndEdit)
            # changes text in static box to value in 'textvalue'
            win32gui.SetWindowText(hwndStatic, textvalue)

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)


wc = win32gui.WNDCLASS()
wc.style = 0
wc.lpfnWndProc = WndProc
wc.hInstance = 0 #hInstance
wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
wc.lpszClassName = "myWindowClass"

atom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(atom, "Edit Box Demo",
                               win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                               win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 700, 350,
                               0, 0, 0, None)  # hInstance, NULL
# 3 child windows are registered
hwndEdit = win32gui.CreateWindow(
    WC_EDIT, None,
    win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER,
    20, 60, 250, 30, hwnd, ID_EDIT, None, None)  # edit control
hwndStatic = win32gui.CreateWindow(
    WC_STATIC, None,
    win32con.WS_BORDER | win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.SS_LEFT,
    20, 20, 250, 30, hwnd, 1, None, None)  # static control
hwndButton = win32gui.CreateWindow(
    WC_BUTTON, "Click Me",
    win32con.WS_VISIBLE | win32con.WS_CHILD,
    20, 100, 80, 30, hwnd, ID_BUTTON, None, None)  # click button

win32gui.PumpMessages()