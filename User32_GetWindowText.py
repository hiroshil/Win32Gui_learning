import win32gui
import win32con
import win32api
# modified from previous example using AI and edited by me

edit_hwnd = int()

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_COMMAND and wParam == 102: # Assuming 102 is the ID of the submit button
        text = win32gui.GetWindowText(edit_hwnd)
        print(text)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "MyWindowClass"
    wc.lpfnWndProc = WndProc
    class_atom = win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(class_atom, "My Window", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                                 100, 100, 300, 200, 0, 0, 0, None)
    
    # Create an edit text control
    global edit_hwnd
    edit_hwnd = win32gui.CreateWindow("EDIT", "", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER,
                                        20, 20, 200, 20, hwnd, 101, 0, None) # 101 is the ID for the edit control

    # Create a button
    button_hwnd = win32gui.CreateWindow("BUTTON", "Submit", win32con.WS_VISIBLE | win32con.WS_CHILD,
                                       20, 60, 80, 25, hwnd, 102, 0, None) # 102 is the ID for the button


    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()