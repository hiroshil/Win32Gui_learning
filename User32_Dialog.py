import win32api
import win32con
import win32gui
# based on nexus-6's c++ code, converted to python code by AI and modified by me

WC_BUTTON = "Button"

IDD_MODELESS = 103
IDD_MODAL = 104
IDC_RED = 1010
IDC_YELLOW = 1011
IDC_GREEN = 1012
IDC_STATIC1 = 1013
# https://stackoverflow.com/questions/2270196/c-win32api-creating-a-dialog-box-without-resource
# https://github.com/krazybean/message_agent_abandoned/blob/master/win/wintest.py#L284
TEMPLATE_MODELESS = [
                        ['Modeless Dialog', (0, 0, 186, 90), win32con.WS_VISIBLE | win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT, None, (8, 'MS Sans Serif')],
                        ["Button", "Red", IDC_RED, (13, 28, 84, 10), win32con.WS_VISIBLE | win32con.BS_AUTORADIOBUTTON],
                        ["Button", "Yellow", IDC_YELLOW, (13, 46, 84, 10), win32con.WS_VISIBLE | win32con.BS_AUTORADIOBUTTON],
                        ["Button", "Green", IDC_GREEN, (13, 63, 84, 10), win32con.WS_VISIBLE | win32con.BS_AUTORADIOBUTTON],
                        ["Button", "choose colour", IDC_STATIC1, (5, 12, 140, 68), win32con.WS_VISIBLE | win32con.BS_GROUPBOX | win32con.WS_TABSTOP]
                    ]

TEMPLATE_MODAL = [
                    ['Model Dialog', (0, 0, 186, 90), win32con.WS_VISIBLE | win32con.DS_SYSMODAL | win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT, None, (8, 'MS Sans Serif')],
                    ["Static", "", IDC_STATIC1, (26, 23, 75, 16), win32con.WS_VISIBLE]
                ]
hBrush = None

class MainWindow:
    def __init__(self, hInstance):
        # dialog demo
        self.hInstance = hInstance
        self.bk_color = win32api.RGB(255, 255, 255)
        self.create_main_window()

    def create_main_window(self):
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = "myWindowClass"
        wc.hInstance = self.hInstance
        wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
        wc.lpfnWndProc = self.WndProc
        win32gui.RegisterClass(wc)

        self.hwnd = win32gui.CreateWindow("myWindowClass", "Dialog box demo", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE, 100, 100, 700, 200, 0, 0, self.hInstance, None)
        
        # Moved the register and create to here
        self.modeless_dialog = ModelessDialog(self.hwnd)
        self.modal_dialog = ModalDialog(self.hwnd)
        
        button_modeless = win32gui.CreateWindow(WC_BUTTON, "Show modeless",win32con.WS_VISIBLE | win32con.WS_CHILD, 20,50,130,35, self.hwnd, IDD_MODELESS, self.hInstance,None)
        button_modal = win32gui.CreateWindow(WC_BUTTON, "Show modal",win32con.WS_VISIBLE | win32con.WS_CHILD, 160,50,130,35, self.hwnd, IDD_MODAL, self.hInstance, None)
        global hBrush
        hBrush = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)

        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW) # show the main window
        
        win32gui.UpdateWindow(self.hwnd) # update the main window

    def WndProc(self, hwnd, msg, wParam, lParam):
        if msg == win32con.WM_PAINT:
            hdc, ps = win32gui.BeginPaint(hwnd)
            win32gui.EndPaint(hwnd, ps)

        # Erases window background with colour in hBrush
        elif msg == win32con.WM_ERASEBKGND:
            hdc = wParam
            rc = win32gui.GetClientRect(hwnd)
            win32gui.FillRect(hdc, rc, hBrush)
            win32gui.ReleaseDC(hwnd, hdc)

        # responds to buttons click
        elif msg == win32con.WM_COMMAND:
          if wParam == IDD_MODELESS:
            self.modeless_dialog.show()
          elif wParam == IDD_MODAL:
            self.modal_dialog.show()
          
        elif msg == win32con.WM_DESTROY:
            win32gui.DeleteObject(hBrush)
            win32gui.PostQuitMessage(0)
            return 0

        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
    def run(self):
        win32gui.PumpMessages()

class ModelessDialog:
    def __init__(self, parent_hwnd):
        self.parent_hwnd = parent_hwnd
        self.bk_color = win32api.RGB(255, 255, 255)
        self.RegisterModelessDialogClass()
        
    # register modeless dialog class
    def RegisterModelessDialogClass(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.ModelessDialogProc
        wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
        wc.lpszClassName = "ModelessDialogClass"
        win32gui.RegisterClass(wc)

    # creates and shows modeless dialog window
    def show(self):
        self.hwnd = win32gui.CreateDialogIndirect(0, TEMPLATE_MODELESS, self.parent_hwnd, self.ModelessDialogProc)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    # modeless callback function
    def ModelessDialogProc(self, hwnd, msg, wParam, lParam):
        mainwnd = win32gui.GetParent(hwnd)
        if msg == win32con.WM_INITDIALOG:
            win32gui.SetFocus(hwnd)
            return True

        elif msg == win32con.WM_COMMAND:
            # responds to radio button click 
            if win32api.HIWORD(wParam) == win32con.BN_CLICKED:
                if win32api.LOWORD(wParam) == IDC_RED: # red button selected.
                    self.bk_color = win32api.RGB(255, 0, 0)
                elif win32api.LOWORD(wParam) == IDC_YELLOW: # yellow button selected
                    self.bk_color = win32api.RGB(255, 255, 0)
                elif win32api.LOWORD(wParam) == IDC_GREEN: # grey button selected
                    self.bk_color = win32api.RGB(0, 255, 0)

                global hBrush
                hBrush = win32gui.CreateSolidBrush(self.bk_color)
                win32gui.InvalidateRect(mainwnd, None, True)
        elif msg == win32con.WM_CLOSE:
            win32gui.DestroyWindow(hwnd) # destroy dialog window
            return True
        return 0

class ModalDialog:
    def __init__(self, parent_hwnd):
        self.parent_hwnd = parent_hwnd
        self.RegisterModalDialogClass() 
    
    # register modal dialog class
    def RegisterModalDialogClass(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.ModalDialogProc
        wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
        wc.lpszClassName = "DialogClass"
        win32gui.RegisterClass(wc)

    # creates and shows modal dialog window
    def show(self):
        win32gui.DialogBoxIndirect(0, TEMPLATE_MODAL, self.parent_hwnd, self.ModalDialogProc)
        
    # modal callback function
    def ModalDialogProc(self, hwnd, msg, wParam, lParam):
      mainwnd = win32gui.GetParent(hwnd)
      words = "A simple demonstration of a modal dialog window."
      if msg == win32con.WM_INITDIALOG:
          staticbox = win32gui.GetDlgItem(hwnd, IDC_STATIC1)
          win32gui.SetWindowText(staticbox, words)
          return 0
      elif msg == win32con.WM_CLOSE:
          win32gui.EndDialog(hwnd, 0) #destroy dialog window
          return True
      return 0
    

def main():
    hInstance = win32api.GetModuleHandle(None)
    main_window = MainWindow(hInstance)
    main_window.run()

if __name__ == "__main__":
    main()