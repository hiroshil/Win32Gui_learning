import win32gui
import win32con
import win32api

listbox_hwnd = int()  # Store the listbox handle

def WndProc(hwnd, msg, wParam, lParam):
    global listbox_hwnd
    if msg == win32con.WM_COMMAND and wParam == 102:  # Assuming 102 is the ID of the submit button
        # Get selected items from the listbox
        selected_idx = win32gui.SendMessage(listbox_hwnd, win32con.LB_GETCARETINDEX, 0, 0)
        print(selected_idx)

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

    # Create a listbox control
    global listbox_hwnd
    listbox_hwnd = win32gui.CreateWindowEx(0, "LISTBOX", "",
                                            win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER | win32con.LBS_STANDARD | win32con.LBS_NOTIFY,  # Extended selection
                                            20, 20, 200, 80, hwnd, 101, 0, None)
    # Add some items to the listbox
    win32gui.SendMessage(listbox_hwnd, win32con.LB_ADDSTRING, 0, "Item 1")
    win32gui.SendMessage(listbox_hwnd, win32con.LB_ADDSTRING, 0, "Item 2")
    win32gui.SendMessage(listbox_hwnd, win32con.LB_ADDSTRING, 0, "Item 3")

    # Create a button
    button_hwnd = win32gui.CreateWindow("BUTTON", "Submit", win32con.WS_VISIBLE | win32con.WS_CHILD,
                                       20, 120, 80, 25, hwnd, 102, 0, None)

    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()