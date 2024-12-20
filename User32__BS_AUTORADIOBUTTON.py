import win32gui
import win32api
import win32con
# based on nexus-6's c++ code, converted to python code by AI

WC_BUTTON = "Button"
ID_BLUE = 1
ID_YELLOW = 2
ID_RED = 3

def WndProc(hwnd, msg, wParam, lParam):
    global bk_color

    if msg == win32con.WM_COMMAND:
        # Responds to button click by setting variable bk_color to value of colour associated with radio button
        if win32api.HIWORD(wParam) == win32con.BN_CLICKED:
            if win32api.LOWORD(wParam) == ID_BLUE:
                bk_color = win32api.RGB(0, 76, 255)
            elif win32api.LOWORD(wParam) == ID_YELLOW:
                bk_color = win32api.RGB(255, 255, 0)
            elif win32api.LOWORD(wParam) == ID_RED:
                bk_color = win32api.RGB(255, 0, 0)

            hdc = win32gui.GetDC(hwnd)
            win32gui.SetBkColor(hdc, bk_color)
            theRect = win32gui.GetClientRect(hwnd)
            win32gui.InvalidateRect(hwnd, theRect, True)
            win32gui.ReleaseDC(hwnd, hdc)

    elif msg == win32con.WM_PAINT:
        # Set background of window to colour selected by radiobutton selection ie red blue or yellow
        hdc, ps = win32gui.BeginPaint(hwnd)
        hBrush = win32gui.CreateSolidBrush(bk_color)
        theRect = win32gui.GetClientRect(hwnd)
        win32gui.FillRect(hdc, theRect, hBrush)
        win32gui.DeleteObject(hBrush)
        win32gui.EndPaint(hwnd, ps)

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

hwnd = win32gui.CreateWindow(atom, "Radio Button Demo",
                               win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                               win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 700, 200,
                               0, 0, 0, None)  # hInstance, NULL
bk_color = win32api.RGB(255, 255, 255)
# Create grouping box and associated buttons
win32gui.CreateWindow(WC_BUTTON, "Choose colour", 
                       win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_GROUPBOX, 
                       50, 25, 300, 70, hwnd, 0, None, None)
win32gui.CreateWindow(WC_BUTTON, "Blue", 
                       win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_AUTORADIOBUTTON, 
                       70, 50, 75, 30, hwnd, ID_BLUE, None, None)
win32gui.CreateWindow(WC_BUTTON, "Yellow", 
                       win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_AUTORADIOBUTTON, 
                       145, 50, 85, 30, hwnd, ID_YELLOW, None, None)
win32gui.CreateWindow(WC_BUTTON, "Red", 
                       win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_AUTORADIOBUTTON, 
                       230, 50, 75, 30, hwnd, ID_RED, None, None)

win32gui.PumpMessages()