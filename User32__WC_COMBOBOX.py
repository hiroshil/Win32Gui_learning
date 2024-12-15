import win32gui
import win32con
import win32api
import math
from ctypes import windll
from ctypes import wintypes

# Define the GetDeviceCaps function signature
GetDeviceCaps = windll.gdi32.GetDeviceCaps
GetDeviceCaps.argtypes = [wintypes.HDC, wintypes.INT]
GetDeviceCaps.restype = wintypes.INT

combo_hwnd = int()  # Store the combobox handle

def WndProc(hwnd, msg, wParam, lParam):
    global combo_hwnd
    if msg == win32con.WM_COMMAND and wParam == 102:  # Assuming 102 is the ID of the submit button
        # Get selected item from the combobox
        item_index = win32gui.SendMessage(combo_hwnd, win32con.CB_GETCURSEL, 0, 0)
        print(item_index)

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    dpiX = 0
    dpiY = 0
    hdc = win32gui.GetDC(0)  # 0 represents the entire screen
    if hdc:
        dpiX = GetDeviceCaps(hdc, win32con.LOGPIXELSX)
        dpiY = GetDeviceCaps(hdc, win32con.LOGPIXELSY)
        win32gui.ReleaseDC(0, hdc)

    width = int(math.ceil(640.0 * dpiX / 96.0))
    height = int(math.ceil(480.0 * dpiY / 96.0))
    
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "MyWindowClass"
    wc.lpfnWndProc = WndProc
    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(class_atom, "My Window", win32con.WS_OVERLAPPEDWINDOW,
                                win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, width, height, 0, 0, 0, None)

    # Example combobox creation (adjust xpos, ypos, nwidth, nheight, hwndParent)
    xpos, ypos = 10, 10  # Example position
    nwidth, nheight = 100, 20 # Example size
    hwndParent = hwnd # Set parent to the main window
    
    # Create a listbox control
    global combo_hwnd
    combo_hwnd = win32gui.CreateWindow("COMBOBOX", "",
                                            win32con.CBS_DROPDOWN | win32con.CBS_HASSTRINGS | win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_OVERLAPPED, # Style
                                            xpos, ypos, nwidth, nheight, hwndParent, 101, 0, None)
    # Add some items to the listbox
    win32gui.SendMessage(combo_hwnd, win32con.CB_ADDSTRING, 0, "Item 1")
    win32gui.SendMessage(combo_hwnd, win32con.CB_ADDSTRING, 0, "Item 2")
    win32gui.SendMessage(combo_hwnd, win32con.CB_ADDSTRING, 0, "Item 3")

    # Send the CB_SETCURSEL message to display an initial item in the selection field  
    win32gui.SendMessage(combo_hwnd, win32con.CB_SETCURSEL, 2, 0)
    
    # Create a button
    button_hwnd = win32gui.CreateWindow("BUTTON", "Submit", win32con.WS_VISIBLE | win32con.WS_CHILD,
                                       20, 120, 80, 25, hwnd, 102, 0, None)

    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()