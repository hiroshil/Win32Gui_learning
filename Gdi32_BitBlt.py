import win32api
import win32con
import win32gui
import random
# based on nexus-6's c++ code, converted to python code by AI and modified by me

memdc = None

def WndProc(hwnd, msg, wParam, lParam):
    global memdc

    if msg == win32con.WM_CREATE:
        lpRect = win32gui.GetClientRect(hwnd)
        maxX = lpRect[2] - lpRect[0]
        maxY = lpRect[3] - lpRect[1]
        
        hdc = win32gui.GetDC(hwnd)  # create a device context
        memdc = win32gui.CreateCompatibleDC(hdc)  # creates a compatible device context copy
        hbit = win32gui.CreateCompatibleBitmap(hdc, maxX, maxY)  # creates bitmap of current device context
        win32gui.SelectObject(memdc, hbit)  # copies device content bitmap into device context copy
        win32gui.PatBlt(memdc, 0, 0, maxX, maxY, win32con.PATCOPY)  # copy current brush into device context copy
        
        # creates 200 random lines in device context copy
        for _ in range(200):
            randx = random.randint(1, maxX)
            randy = random.randint(1, maxY)
            win32gui.LineTo(memdc, randx, randy)

        win32gui.ReleaseDC(hwnd, hdc)
    
    elif msg == win32con.WM_PAINT:
        # copies compatible device image into device context before repainting window
        hdc, ps = win32gui.BeginPaint(hwnd)
        win32gui.BitBlt(hdc, ps[2][0], ps[2][1], # ps.rcPaint.left, ps.rcPaint.top
                        ps[2][2] - ps[2][0], # ps.rcPaint.right - ps.rcPaint.left 
                        ps[2][3] - ps[2][1], # ps.rcPaint.bottom - ps.rcPaint.top
                        memdc, ps[2][0], ps[2][1], # ps.rcPaint.left, ps.rcPaint.top
                        win32con.SRCCOPY)
        win32gui.EndPaint(hwnd, ps)
    
    elif msg == win32con.WM_DESTROY:
        win32gui.ReleaseDC(hwnd, memdc)
        win32gui.PostQuitMessage(0)
        return 0

    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = WndProc
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.lpszClassName = "myWindowClass"
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
    
    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(wc.lpszClassName, "Text Output", 
                                  win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
                                  win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 
                                  700, 200, 0, 0, wc.hInstance, None)
    
    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

