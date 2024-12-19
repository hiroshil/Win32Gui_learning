import win32api
import win32con
import win32gui
# based on nexus-6's c++ code, converted to python code by AI

def WndProc(hwnd, msg, wParam, lParam):
    dc = None
    ps = None
    if msg == win32con.WM_PAINT:
        dc, ps = win32gui.BeginPaint(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        
        # Draw rectangle with default pen
        win32gui.Rectangle(dc, 100, 100, 300, 300)

        # Draw rectangle with red pen using mapping mode MM_HIMETRIC
        linecolor = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(255, 0, 0))
        win32gui.SelectObject(dc, linecolor)
        win32gui.SetMapMode(dc, win32con.MM_HIMETRIC)
        win32gui.Rectangle(dc, 100, -100, 300, -300)
        win32gui.DeleteObject(linecolor)

        # Draw rectangle with blue pen using mapping mode MM_LOMETRIC
        linecolor1 = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(0, 0, 255))
        win32gui.SelectObject(dc, linecolor1)
        win32gui.SetMapMode(dc, win32con.MM_LOMETRIC)
        win32gui.Rectangle(dc, 100, -100, 300, -300)
        win32gui.DeleteObject(linecolor1)

        # Draw rectangle with purple pen using mapping mode MM_LOENGLISH
        linecolor2 = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(255, 0, 255))
        win32gui.SetMapMode(dc, win32con.MM_LOENGLISH)
        win32gui.SelectObject(dc, linecolor2)
        win32gui.Rectangle(dc, 100, -100, 300, -300)
        win32gui.DeleteObject(linecolor2)

        # Draw rectangle with blue pen and PS_DASH pen style using mapping mode MM_ANISOTROPIC
        win32gui.SetMapMode(dc, win32con.MM_ANISOTROPIC)
        win32gui.SetWindowExtEx(dc, 1, 10)
        win32gui.SetViewportExtEx(dc, 1, 1)
        linecolor3 = win32gui.CreatePen(win32con.PS_DASH, 1, win32api.RGB(0, 0, 255))
        win32gui.SelectObject(dc, linecolor3)
        win32gui.Rectangle(dc, 100, 300, 300, 500)
        win32gui.DeleteObject(linecolor3)

        win32gui.EndPaint(hwnd, ps)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0

    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

wc = win32gui.WNDCLASS()
wc.style = 0
wc.lpfnWndProc = WndProc
wc.hInstance = win32api.GetModuleHandle(None)
wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
wc.lpszClassName = "myWindowClass"

classAtom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(classAtom, "Mapping Mode", win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
                                win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 700, 350, 0, 0, wc.hInstance, None)

win32gui.PumpMessages()