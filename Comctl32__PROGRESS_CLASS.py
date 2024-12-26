import win32api
import win32con
import win32gui
import commctrl
from ctypes import windll, wintypes, WINFUNCTYPE, c_uint
# based on nexus-6's c++ code, converted to python code by Google's AI and modified by me

WC_BUTTON = "Button"

# Define the types for the SetTimer function parameters
UINT_PTR = c_uint
TIMERPROC = WINFUNCTYPE(None, wintypes.HWND, wintypes.UINT, UINT_PTR, wintypes.DWORD)
# Define the SetTimer function
SetTimer = windll.user32.SetTimer
# Set the argument types and return type
SetTimer.argtypes = [wintypes.HWND, UINT_PTR, wintypes.UINT, TIMERPROC]
SetTimer.restype = UINT_PTR

# Define the function signature
KillTimer = windll.user32.KillTimer
KillTimer.argtypes = [wintypes.HWND, UINT_PTR]
KillTimer.restype = wintypes.BOOL

ID_TIMER = 2

# progress bar example
class ProgressBarWindowProc:
    def __init__(self):
        self.hwndPrgBar = None
        self.hbtn = None
        self.c = 0
        self.hwnd = None
        # message handler
        self.defaultMessage = True
        self.wndproc = {
            win32con.WM_CREATE: self.OnCreate,
            win32con.WM_TIMER: self.OnTimer,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_DESTROY: self.OnDestroy,
        }
    def OnCreate(self, hwnd, msg, wparam, lparam):
      self.CreateControls(hwnd)
    def CreateControls(self, hwnd):
      # load common control class ICC_PROGRESS_CLASS from the dynamic-link library (DLL).
      win32gui.InitCommonControlsEx(commctrl.ICC_PROGRESS_CLASS)

      #create pager window
      self.hwndPrgBar = win32gui.CreateWindow(
        commctrl.PROGRESS_CLASS, None, 
        win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.PBS_SMOOTH, 
        30, 20, 190, 25, hwnd, None, None, None
      )
      self.hbtn = win32gui.CreateWindow(
        WC_BUTTON, "Start", 
        win32con.WS_CHILD | win32con.WS_VISIBLE, 
        85, 90, 85, 25, hwnd, None, None, None
      )
      #set range of pager windows to 100
      win32gui.SendMessage(self.hwndPrgBar, commctrl.PBM_SETRANGE, 0, win32api.MAKELONG(0, 100))
      #set step increment in page window progression
      win32gui.SendMessage(self.hwndPrgBar, commctrl.PBM_SETSTEP, 1, 0)

    def OnTimer(self, hwnd, msg, wparam, lparam):
      #Advances the current position for a progress bar by the step increment and redraws the bar to reflect the new position
      win32gui.SendMessage(self.hwndPrgBar, commctrl.PBM_STEPIT, 0, 0)
      self.c += 1
      if self.c == 100:
        KillTimer(hwnd, ID_TIMER)
        win32gui.SendMessage(self.hbtn, win32con.WM_SETTEXT, 0, "Start")
        self.c = 0
    def OnCommand(self, hwnd, msg, wparam, lparam):
      if self.c == 0:
        self.c = 1
        win32gui.SendMessage(self.hwndPrgBar, commctrl.PBM_SETPOS, 0, 0)
        SetTimer(hwnd, ID_TIMER, 5, TIMERPROC())
        win32gui.SendMessage(self.hbtn, win32con.WM_SETTEXT, 0, "In progress")
    def OnDestroy(self, hwnd, msg, wparam, lparam):
      KillTimer(hwnd, ID_TIMER)
      win32gui.PostQuitMessage(0)
    
    def __call__(self, hwnd, msg, wparam, lparam):
      if msg in self.wndproc:
          self.wndproc[msg](hwnd, msg, wparam, lparam)
      return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    
def main():
    wndclass = win32gui.WNDCLASS()
    wndclass.lpszClassName = "Progress bar"
    wndclass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wndclass.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
    wndclass.lpfnWndProc = ProgressBarWindowProc()
    wndclass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    win32gui.RegisterClass(wndclass)

    hwnd = win32gui.CreateWindow(
        wndclass.lpszClassName, "Progress bar",
        win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
        100, 100, 260, 170, 0, 0, 0, None
    )
    
    win32gui.SendMessage(hwnd, win32con.WM_CREATE, 0, 0) # fix WM_CREATE not initialized in pywin32
    
    win32gui.PumpMessages()
if __name__ == "__main__":
    main()