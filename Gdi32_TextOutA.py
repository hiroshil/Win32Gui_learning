import win32api
import win32con
import win32gui
from ctypes import windll, wintypes, create_string_buffer, cast, sizeof, c_char_p, c_int
# based on nexus-6's c++ code

# Define the TextOutW function prototype
TextOut = windll.gdi32.TextOutA

# Define the argument types
TextOut.argtypes = [
    wintypes.HDC,  # hdc
    c_int,  # x
    c_int,  # y
    wintypes.LPCWSTR,  # lpString
    c_int  # c
]

# Define the return type
TextOut.restype = wintypes.BOOL

# Define necessary types
LPCSTR = c_char_p
DWORD = wintypes.DWORD
HFONT = wintypes.HANDLE

# Define the CreateFontA function signature
CreateFont = windll.gdi32.CreateFontA
CreateFont.argtypes = [
    c_int,  # cHeight
    c_int,  # cWidth
    c_int,  # cEscapement
    c_int,  # cOrientation
    c_int,  # cWeight
    DWORD,  # bItalic
    DWORD,  # bUnderline
    DWORD,  # bStrikeOut
    DWORD,  # iCharSet
    DWORD,  # iOutPrecision
    DWORD,  # iClipPrecision
    DWORD,  # iQuality
    DWORD,  # iPitchAndFamily
    LPCSTR  # pszFaceName
]
CreateFont.restype = HFONT

def WndProc(hwnd, msg, wParam, lParam):
    x = 0
    y = 0
    try:
        if msg == win32con.WM_PAINT:
            hdc, ps = win32gui.BeginPaint(hwnd)
            
            # save current device context
            hDCLast = win32gui.SaveDC(hdc)
            
            # Output text using default font
            txt = "Stock font"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, 0, y, cast(buf, wintypes.LPCWSTR), len(txt))
            
            # Select ANSI_FIXED_FONT and output text
            tm = win32gui.GetTextMetrics(hdc)
            y += tm.get("Height")
            hBrush = win32gui.GetStockObject(win32con.ANSI_FIXED_FONT)
            win32gui.SelectObject(hdc, hBrush)
            txt = "ANSI_FIXED_FONT"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, 0, y, cast(buf, wintypes.LPCWSTR), len(txt))
            
            # Output text with different colors and backgrounds
            tm = win32gui.GetTextMetrics(hdc)
            y += tm.get("Height")
            win32gui.SetTextColor(hdc, win32api.RGB(255, 0, 0))  # red
            txt = "ANSI_FIXED_FONT, color red"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, x, y, cast(buf, wintypes.LPCWSTR), len(txt))
            
            # Set text background to colour blue and output text
            tm = win32gui.GetTextMetrics(hdc)
            y += tm.get("Height")
            win32gui.SetBkColor(hdc, win32api.RGB(0, 0, 255))  # blue
            txt = "ANSI_FIXED_FONT, color red with blue background"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, x, y, cast(buf, wintypes.LPCWSTR), len(txt))

            # Set text background to transparent and output text
            tm = win32gui.GetTextMetrics(hdc)
            y += tm.get("Height")
            win32gui.SetBkMode(hdc, win32con.TRANSPARENT)
            txt = "ANSI_FIXED_FONT, color red, transparent background"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, 0, y, cast(buf, wintypes.LPCWSTR), len(txt))
            
            # Select font Ariel 20 and output text
            tm = win32gui.GetTextMetrics(hdc)
            y += tm.get("Height")
            font = CreateFont(20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"Ariel")
            hFontOld = win32gui.SelectObject(hdc, font)
            txt = "ANSI_FIXED_FONT, colour red, transparent background,arial 20"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, 0, y, cast(buf, wintypes.LPCWSTR), len(txt))
            
            # Restore default font using saved value and output text
            tm = win32gui.GetTextMetrics(hdc)
            y += tm.get("Height")
            win32gui.RestoreDC(hdc, hDCLast)
            txt = "stock font restored using SaveDC/RestoreDC"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, x, y, cast(buf, wintypes.LPCWSTR), len(txt))
            y += tm.get("Height") # Calculate new vertical coordinate using text metric
            
            # Select font times new romans 30 and output text
            font = CreateFont(30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"Times New Roman")
            win32gui.SelectObject(hdc, font)
            tm = win32gui.GetTextMetrics(hdc)
            baseline = tm.get("Ascent") # used to calculate font baseline
            txt = "times new roman 30 statement 1"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, x, y, cast(buf, wintypes.LPCWSTR), len(txt))
            size = win32gui.GetTextExtentPoint32(hdc, txt)
            x += size[0]
            
            # Select font courier new 20 and output text
            font = CreateFont(20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"Courier New")
            win32gui.SelectObject(hdc, font)
            tm = win32gui.GetTextMetrics(hdc)
            baselinecourier = baseline - tm.get("Ascent") # used to calculate font baseline
            txt = "Courier statement 2"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, x, y + baselinecourier, cast(buf, wintypes.LPCWSTR), len(txt))
            size = win32gui.GetTextExtentPoint32(hdc, txt)
            x += size[0]
            
            # Select font ariel 20 and output text
            font = CreateFont(10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"Ariel")
            win32gui.SelectObject(hdc, font)
            tm = win32gui.GetTextMetrics(hdc)
            baselineariel = baseline - tm.get("Ascent") # used to calculate font baseline
            txt = "ariel 10 statement 3"
            buf = create_string_buffer(txt.encode('utf-8'))
            TextOut(hdc, x, y + baselineariel, cast(buf, wintypes.LPCWSTR), len(txt))
            
            win32gui.EndPaint(hwnd, ps)
            
            win32gui.DeleteObject(font)
            win32gui.DeleteObject(hBrush)

        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0

        elif msg == win32con.WM_CLOSE:
            win32gui.DestroyWindow(hwnd)
            return 0

    except Exception as e:
      print(f"Exception in WndProc: {e}")


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
    "Text Output",
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

# Show & update the window
win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
win32gui.UpdateWindow(hwnd)

# Dispatch messages
win32gui.PumpMessages()