import win32gui
import win32api
import win32con
import win32file

ID_BUTTON = 1
ID_BUTTON1 = 2

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_COMMAND:
        if win32api.LOWORD(wParam) == ID_BUTTON:
            OpenDialog(hwnd)
        elif win32api.LOWORD(wParam) == ID_BUTTON1:
            SaveDialog(hwnd)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def OpenDialog(hwnd):
    ofn = dict()
    ofn.update(hwndOwner = hwnd)
    ofn.update(Filter = "All Files\0*.*\0Text Files\0*.TXT\0")
    ofn.update(FilterIndex = 1)
    ofn.update(Flags = win32con.OFN_PATHMUSTEXIST | win32con.OFN_FILEMUSTEXIST)

    try:
        file = win32gui.GetOpenFileNameW(**ofn)
        hFile = win32file.CreateFile(file[0], win32con.GENERIC_READ, 0, None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None)
        win32file.CloseHandle(hFile)
    except BaseException as e:
        if e.winerror == 0:
            return
        else:
            raise IOError()

def SaveDialog(hwnd):
    ofn = dict()
    ofn.update(hwndOwner = hwnd)
    ofn.update(Filter = "Text Files (*.txt)\0*.txt\0All Files (*.*)\0*.*\0")
    ofn.update(Flags = win32con.OFN_EXPLORER | win32con.OFN_PATHMUSTEXIST | win32con.OFN_HIDEREADONLY | win32con.OFN_OVERWRITEPROMPT)
    ofn.update(DefExt = "txt")

    try:
        file = win32gui.GetSaveFileNameW(**ofn)
        hFile = win32file.CreateFile(file[0], win32con.GENERIC_READ | win32con.GENERIC_WRITE, win32con.FILE_SHARE_READ, None, win32con.OPEN_ALWAYS, win32con.FILE_ATTRIBUTE_NORMAL, None)
        dwByteCount = win32file.WriteFile(hFile, "Common dialog demo".encode('utf-16'), None)
        win32file.CloseHandle(hFile)
    except BaseException as e:
        if e.winerror == 0:
            return
        else:
            raise IOError()

def main():
    wc = win32gui.WNDCLASS()
    wc.style = 0
    wc.lpfnWndProc = WndProc
    wc.hInstance = win32api.GetModuleHandle()
    wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.lpszClassName = "myWindowClass"

    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(wc.lpszClassName, "File open/save dialog box", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE, 150, 150, 250, 200, 0, 0, wc.hInstance, None)

    win32gui.CreateWindow("button", "File Open", win32con.WS_VISIBLE | win32con.WS_CHILD, 20, 30, 80, 25, hwnd, ID_BUTTON, None, None)
    win32gui.CreateWindow("button", "File save", win32con.WS_VISIBLE | win32con.WS_CHILD, 120, 30, 80, 25, hwnd, ID_BUTTON1, None, None)
    
    # Show & update the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    # Dispatch messages
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()

