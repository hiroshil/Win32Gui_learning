import win32gui
import win32api
import win32con
from ctypes import windll, wintypes, create_string_buffer, cast, c_int
# based on nexus-6's c++ code, converted to python code by AI and modified by me

# Define the TextOutW function prototype
TextOutA = windll.gdi32.TextOutA
# Define the argument types
TextOutA.argtypes = [
    wintypes.HDC,  # hdc
    c_int,  # x
    c_int,  # y
    wintypes.LPCWSTR,  # lpString
    c_int  # c
]
# Define the return type
TextOutA.restype = wintypes.BOOL

# Define the GetScrollPos function
GetScrollPos = windll.user32.GetScrollPos
GetScrollPos.argtypes = [wintypes.HWND, c_int]
GetScrollPos.restype = c_int

# Define the function signature
SetScrollRange = windll.user32.SetScrollRange
SetScrollRange.argtypes = [
    wintypes.HWND,  # hWnd
    c_int,   # nBar
    c_int,   # nMinPos
    c_int,   # nMaxPos
    wintypes.BOOL   # bRedraw
]
SetScrollRange.restype = wintypes.BOOL

def TextOut(hdc, x, y, txt, size):
    buf = create_string_buffer(txt.encode('utf-8'))
    TextOutA(hdc, x, y, cast(buf, wintypes.LPCWSTR), size)

def WndProc(hwnd, msg, wParam, lParam):
    totalrows = 100
    rows = 0

    # Traps paint message
    if msg == win32con.WM_PAINT:
        hdc, ps = win32gui.BeginPaint(hwnd)
        linecount = 0
        startline = GetScrollPos(hwnd, win32con.SB_VERT)
        # fix not initializing WM_SIZE values in pywin32
        rc = win32gui.GetClientRect(hwnd)
        yClient = rc[3] - 4
        rows = yClient // 15
        SetScrollRange(hwnd, win32con.SB_VERT, 0, totalrows - rows, True)
        endline = startline + rows

        # Output line number
        for count in range(startline, endline):
            sbv = str(count + 1)
            TextOut(hdc, 0, linecount, sbv, len(sbv))
            linecount += 15

        win32gui.EndPaint(hwnd, ps)

    # Deals with changes in widows size
    elif msg == win32con.WM_SIZE:
        yClient = win32gui.HIWORD(lParam) # Retrieves the height of the client area.
        rows = yClient // 15 # Calculate totoal number of text row in client area
        SetScrollRange(hwnd, win32con.SB_VERT, 0, totalrows - rows, True) # Set scrollbar size
        win32gui.InvalidateRect(hwnd, None, True) # Repaint window

    elif msg == win32con.WM_VSCROLL:
        # Retrieves attributes of scrollbar
        si = list(win32gui.GetScrollInfo(hwnd, win32con.SB_VERT))

        # Respond to scrollbar messages
        # User clicked the HOME keyboard key.
        if win32gui.LOWORD(wParam) == win32con.SB_TOP:
            si[4] = si[1] # nPos -> nMin
        # User clicked the END keyboard key.
        elif win32gui.LOWORD(wParam) == win32con.SB_BOTTOM:
            si[4] = si[2] # nPos -> nMax
        # User clicked the top arrow.
        elif win32gui.LOWORD(wParam) == win32con.SB_LINEUP:
            si[4] -= 1 # nPos
        # User clicked the bottom arrow.
        elif win32gui.LOWORD(wParam) == win32con.SB_LINEDOWN:
            si[4] += 1 # nPos
        # User dragged the scroll box.
        elif win32gui.LOWORD(wParam) == win32con.SB_THUMBTRACK:
            si[4] = si[5] # nPos -> nTrackPos

        si[0] = win32con.SIF_POS # fMask
        # Set the new scollbar position.
        win32gui.SetScrollInfo(hwnd, win32con.SB_VERT, tuple(si), True)
        # Redraw window contents by manually sending manually sending WM_PAINT
        win32gui.InvalidateRect(hwnd, None, True)

    elif msg == win32con.WM_CLOSE:
        win32gui.DestroyWindow(hwnd)

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    else:
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

    return 0


wc = win32gui.WNDCLASS()
wc.style = 0
wc.lpfnWndProc = WndProc
wc.hInstance = 0 #hInstance
wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
wc.lpszClassName = "myWindowClass"

atom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(atom, "ScrollBar Demo",
                               win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                               win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 700, 200,
                               0, 0, 0, None)  # hInstance, NULL

win32gui.PumpMessages()