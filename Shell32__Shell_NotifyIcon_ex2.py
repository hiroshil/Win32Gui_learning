# -*- coding: utf-8 -*-
import os

import win32api
import win32con
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

import itertools
import glob
# based on https://github.com/eavatar/eavatar-me/blob/master/src/avashell/win32/shell.py

class MainFrame(object):
    def __init__(self, message_map):
        self.window_class_name = "MainFrame"
        self.hinst = None
        self.class_atom = self.register_wnd_class(message_map)
        self.hwnd = self.create_window()

    def register_wnd_class(self, message_map):
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        self.hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # could also specify a wndproc.
        return win32gui.RegisterClass(window_class)

    def create_window(self):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = win32gui.CreateWindow(self.class_atom,
                                     self.window_class_name,
                                     style,
                                     0,
                                     0,
                                     310,
                                     250,
                                     0,
                                     0,
                                     self.hinst,
                                     None)
        win32gui.UpdateWindow(hwnd)
        return hwnd

    def show(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_NORMAL)

    def close(self):
        win32gui.PostQuitMessage(0)


STR_ITEM1 = u'item 1'
STR_ITEM2 = u'item 2'

STR_EXIT = u'Exit'
STR_STATUS = u'SysTray is running'

STR_EMPTY_MENU = u'Empty Menu'
STR_SUBMENU = u'Submenu'
SUBMENU_ITEM_STRINGS = ["item 1", "item 2", "item 3", "item 4"]

ICO_PATH = u'/content/Win32Gui_learning/ico'

_FIRST_ID = 1023
_ID_ITEM1 = 1024
_ID_ITEM2 = 1026
_ID_ITEM3 = 1027

_ID_SUBMENU_1 = 1040
_ID_SUBMENU_2 = 1041
_ID_SUBMENU_3 = 1042
_ID_SUBMENU_4 = 1043

_ID_QUIT = 1100


class TrayIcon(object):
    def __init__(self, s):
        self.shell = s

        self.icons = itertools.cycle(glob.glob(
            ICO_PATH + '/*.ico'))
        self.hover_text = STR_STATUS

        self.icon = next(self.icons)

        self.notify_id = None
        self.hicon = None
        self.refresh_icon()
        self.submenu = self.create_submenu()

    def refresh_icon(self):
        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            self.hicon = win32gui.LoadImage(hinst,
                                            self.icon,
                                            win32con.IMAGE_ICON,
                                            0,
                                            0,
                                            icon_flags)
        else:
            print("Can't find icon file - using default.")
            self.hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD

        self.notify_id = (self.shell.main_frame.hwnd,
                          0,
                          (win32gui.NIF_ICON | win32gui.NIF_MESSAGE |
                           win32gui.NIF_TIP),
                          win32con.WM_USER + 20,
                          self.hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu)

        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.shell.main_frame.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.shell.main_frame.hwnd,
                                None)

    def update_menu(self, selected_id):
        for i, s in enumerate(SUBMENU_ITEM_STRINGS):
            fstate = 0
            if selected_id == i:
                fstate = win32con.MFS_CHECKED
            item, extras = win32gui_struct.PackMENUITEMINFO(
                text=SUBMENU_ITEM_STRINGS[i],
                hbmpItem=None,
                fState=fstate,
                wID=_ID_SUBMENU_1 + i)
            win32gui.SetMenuItemInfo(self.submenu, i, 1, item)

    def create_submenu(self):
        menu = win32gui.CreateMenu()
        for i, s in enumerate(SUBMENU_ITEM_STRINGS):
            fstate = 0
            if self.shell.selected_id == i:
                fstate = win32con.MFS_CHECKED
            item, extras = win32gui_struct.PackMENUITEMINFO(
                text=SUBMENU_ITEM_STRINGS[i],
                hbmpItem=None,
                fState=fstate,
                wID=_ID_SUBMENU_1 + i)
            win32gui.InsertMenuItem(menu, i, 1, item)

        self.submenu = menu
        return self.submenu

    def create_menu(self, menu):
        item, extras = win32gui_struct.PackMENUITEMINFO(
            text=STR_EXIT,
            hbmpItem=None,
            wID=_ID_QUIT)

        win32gui.InsertMenuItem(menu, 0, 1, item)

        win32gui.InsertMenu(menu, 0, win32con.MF_BYPOSITION,
                            win32con.MF_SEPARATOR, None)

        win32gui.InsertMenu(menu, 0,
                            win32con.MF_POPUP | win32con.MF_BYPOSITION,
                            self.submenu, STR_SUBMENU)

        win32gui.InsertMenu(menu, 0, win32con.MF_BYPOSITION,
                            win32con.MF_SEPARATOR, None)

        item, extras = win32gui_struct.PackMENUITEMINFO(
            text=STR_ITEM2,
            hbmpItem=None,
            wID=_ID_ITEM2)

        win32gui.InsertMenuItem(menu, 0, 1, item)

        item, extras = win32gui_struct.PackMENUITEMINFO(
            text=STR_ITEM1,
            hbmpItem=None,
            wID=_ID_ITEM1)

        win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # First load the icon.
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y,
                                   win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0,
                            win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def switch_icon(self):
        self.icon = next(self.icons)
        self.refresh_icon()


class Shell():
    def __init__(self):

        self.selected_id = int()
        msg_taskbar_restart = win32gui.RegisterWindowMessage("TaskbarCreated")
        self.message_map = {msg_taskbar_restart: self.OnRestart,
                            win32con.WM_DESTROY: self.OnDestroy,
                            win32con.WM_COMMAND: self.OnCommand,
                            win32con.WM_USER + 20: self.OnTaskbarNotify, }

        self.main_frame = MainFrame(self.message_map)
        self.tray_icon = TrayIcon(self)

    def update_selected_id_converted(self, item_id, start_id):
        selected_id = self.selected_id
        self.selected_id = item_id - start_id

        if selected_id == self.selected_id:
            return

        self.tray_icon.update_menu(self.selected_id)

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self.tray_icon.refresh_icon()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.main_frame.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_RBUTTONUP:
            self.tray_icon.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:
            self.execute_menu_option(_FIRST_ID)

        return True

    def execute_menu_option(self, id):
        if id == _FIRST_ID:
            print("right click to use program")
        elif id == _ID_QUIT:
            win32gui.DestroyWindow(self.main_frame.hwnd)
        elif id == _ID_ITEM1:
            print("item 1 clicked!")
            self.tray_icon.switch_icon()
        elif id == _ID_ITEM2:
            print("item 2 clicked!")
        elif id == _ID_ITEM3:
            print("item 3 clicked!")
        elif (_ID_SUBMENU_1 <= id <= _ID_SUBMENU_4):
            self.update_selected_id_converted(id, _ID_SUBMENU_1)
    
    def run(self):
        win32gui.PumpMessages()


if __name__ == '__main__':
    shell = Shell()
    shell.run()
