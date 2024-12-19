import win32gui
import win32api
import win32con
from ctypes import windll, wintypes, create_string_buffer, cast, c_int
# based on nexus-6's c++ code, converted to python code by AI

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

def TextOut(hdc, x, y, txt):
    buf = create_string_buffer(txt.encode('utf-8'))
    TextOutA(hdc, x, y, cast(buf, wintypes.LPCWSTR), len(txt))

def WndProc(hwnd, msg, wParam, lParam):
    hdc = None
    ps = None
    polygon = [(80, 185), (145, 185), (155, 130), (115, 145), (80, 135)]
    bezier = [(320, 180), (370, 180), (375, 130), (400, 130)]
    hbrush = 0
    hpen = 0

    try:
        if msg == win32con.WM_PAINT:
            hdc, ps = win32gui.BeginPaint(hwnd)

            #draws line around window
            win32gui.MoveToEx(hdc, 50, 10)
            win32gui.LineTo(hdc, 620, 10)
            win32gui.LineTo(hdc, 620, 240)
            win32gui.LineTo(hdc, 50, 240)
            win32gui.LineTo(hdc, 50, 10)

            #draws ellipse with default pen and brush
            win32gui.Ellipse(hdc, 80, 30, 170, 90)
            TextOut(hdc, 100, 95, "Ellipse")

            #creates hbrush with colour green and draws roundrect
            hbrush = win32gui.CreateSolidBrush(win32api.RGB(0, 255, 0))
            win32gui.SelectObject(hdc, hbrush)
            win32gui.RoundRect(hdc, 200, 30, 290, 90, 15, 20)
            TextOut(hdc, 180, 95, "Rounded rectangle")

            #creates hbrush with yellow cross hatch and draws chord
            hbrush = win32gui.CreateHatchBrush(win32con.HS_CROSS, win32api.RGB(255, 255, 0))
            win32gui.SelectObject(hdc, hbrush)
            win32gui.Chord(hdc, 320, 30, 410, 90, 320, 45, 410, 45)
            TextOut(hdc, 350, 95, "Chord")

            #creates hbrush white and draws pie
            hbrush = win32gui.CreateSolidBrush(win32api.RGB(255, 255, 255))
            win32gui.SelectObject(hdc, hbrush)
            win32gui.Pie(hdc, 450, 30, 540, 90, 320, 45, 410, 45)
            TextOut(hdc, 485, 95, "Pie")
            
            #creates hbrush with red cross hatch and draws polygon
            hbrush = win32gui.CreateHatchBrush(win32con.HS_VERTICAL, win32api.RGB(255, 0, 0))
            win32gui.SelectObject(hdc, hbrush)
            win32gui.Polygon(hdc, polygon)
            TextOut(hdc, 100, 195, "Polygon")

            #creates hbrush black and draws rectangle
            hbrush = win32gui.CreateSolidBrush(win32api.RGB(0, 0, 0))
            win32gui.SelectObject(hdc, hbrush)
            win32gui.Rectangle(hdc, 200, 130, 280, 180)
            TextOut(hdc, 210, 195, "Rectangle")

            #draws Bezier curve
            win32gui.PolyBezier(hdc, bezier)
            TextOut(hdc, 340, 195, "Bezier")

            #draws 3 lines with 3 different style in 3 different colours
            win32gui.MoveToEx(hdc, 450, 130)
            hpen = win32gui.CreatePen(win32con.PS_DASH, 1, win32api.RGB(0, 0, 255))
            win32gui.SelectObject(hdc, hpen)
            win32gui.LineTo(hdc, 540, 130)
            win32gui.MoveToEx(hdc, 450, 155)
            hpen = win32gui.CreatePen(win32con.PS_DOT, 1, win32api.RGB(255, 0, 255))
            win32gui.SelectObject(hdc, hpen)
            win32gui.LineTo(hdc, 540, 155)
            win32gui.MoveToEx(hdc, 450, 180)
            hpen = win32gui.CreatePen(win32con.PS_DASHDOTDOT, 1, win32api.RGB(255, 0, 0))
            win32gui.SelectObject(hdc, hpen)
            win32gui.LineTo(hdc, 540, 180)
            TextOut(hdc, 480, 195, "Lines")


            win32gui.EndPaint(hwnd, ps)

            if hbrush: win32gui.DeleteObject(hbrush)
            if hpen: win32gui.DeleteObject(hpen)

        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0

        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
    except Exception as e:
        print(f"Error in WndProc: {e}")
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

hwnd = win32gui.CreateWindow(atom, "Displaying Graphics",
                               win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                               win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 700, 300,
                               0, 0, 0, None)  # hInstance, NULL

win32gui.PumpMessages()