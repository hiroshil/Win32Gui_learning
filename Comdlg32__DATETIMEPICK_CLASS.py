import win32api
import win32con
import win32gui
import win32gui_struct
import commctrl
import struct
import array
from ctypes import create_unicode_buffer
# based on nexus-6's c++ code, converted to python code by AI and modified by me

WC_STATIC = "Static"

_systemtime_fmt = "8H"

def EmptySYSTEMTIME():

    # Now copy the string to a writable buffer, so that the result
    # could be passed to a 'Get' function
    buf = struct.pack(
        _systemtime_fmt,
        0,  # wYear
        0,  # wMonth
        0,  # wDayOfWeek
        0,  # wDay
        0,  # wHour
        0,  # wMinute
        0,  # wSecond
        0,  # wMilliseconds
    )
    return array.array("b", buf)

def UnpackSYSTEMTIME(buf):
    return win32gui_struct._MakeResult(
        "SYSTEMTIME wYear wMonth wDayOfWeek wDay wHour wMinute wSecond wMilliseconds", struct.unpack(_systemtime_fmt, buf)
    )

# Global variables
DateHandle = None
TimeHandle = None
hStat = None

def GetSelectedDate(hMonthCal, TimeHandle, hStat):
    time = EmptySYSTEMTIME()
    date = create_unicode_buffer(80)
    
    # Get selected date
    win32gui.SendMessage(hMonthCal, commctrl.DTM_GETSYSTEMTIME, 0, time)
    
    dt = UnpackSYSTEMTIME(time)
    date.value = f"Selected date: {dt.wDay}-{dt.wMonth}-{dt.wYear}"
    
    # Get selected time
    win32gui.SendMessage(TimeHandle, commctrl.DTM_GETSYSTEMTIME, 0, time)
    
    dt = UnpackSYSTEMTIME(time)
    date.value += f"\nSelected time: {dt.wHour}-{dt.wMinute}-{dt.wSecond}"
    
    win32gui.SetWindowText(hStat, date.value)

def WndProc(hwnd, msg, wParam, lParam):
    global DateHandle, TimeHandle, hStat
    if msg == win32con.WM_CREATE:
        
        # Create date time control
        DateHandle = win32gui.CreateWindow(commctrl.DATETIMEPICK_CLASS, "DateTime", win32con.WS_BORDER | win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.DTS_SHOWNONE, 20, 50, 220, 25, hwnd, None, None, None)
        TimeHandle = win32gui.CreateWindow(commctrl.DATETIMEPICK_CLASS, "DateTime", win32con.WS_BORDER | win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.DTS_TIMEFORMAT, 20, 10, 90, 25, hwnd, None, None, None)
        
        # Create static box
        hStat = win32gui.CreateWindow(WC_STATIC, "", win32con.WS_CHILD | win32con.WS_VISIBLE, 20, 130, 280, 35, hwnd, None, None, None)
        win32gui.ShowWindow(DateHandle, win32con.SW_SHOW)

    elif msg == win32con.WM_NOTIFY:
        lpNmHdr = win32gui_struct.UnpackWMNOTIFY(lParam)
        if lpNmHdr.code == commctrl.DTN_DATETIMECHANGE:
            GetSelectedDate(DateHandle, TimeHandle, hStat)

    elif msg == win32con.WM_CLOSE:
        win32gui.DestroyWindow(hwnd)

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)

    else:
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
    
    return 0

def main():
    wc = win32gui.WNDCLASS()
    wc.style = 0
    wc.lpfnWndProc = WndProc
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hIcon = win32gui.LoadIcon(None, win32con.IDI_APPLICATION)
    wc.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.lpszClassName = "myWindowClass"
    
    win32gui.RegisterClass(wc)
    
    hwnd = win32gui.CreateWindow("myWindowClass", "Date and time picker", win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 340, 220, None, None, wc.hInstance, None)
    
    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

