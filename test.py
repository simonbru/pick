import ctypes
import ctypes.wintypes

STD_OUTPUT_HANDLE = -11


class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short),
                ("Y", ctypes.c_short)]


class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short),
                ("Top", ctypes.c_short),
                ("Right", ctypes.c_short),
                ("Bottom", ctypes.c_short)]


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [("dwSize", COORD),
                ("dwCursorPosition", COORD),
                ("wAttributes", ctypes.c_short),
                ("srWindow", SMALL_RECT),
                ("dwMaximumWindowSize", COORD)]


hout = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
info = CONSOLE_SCREEN_BUFFER_INFO()
ctypes.windll.kernel32.GetConsoleScreenBufferInfo(
    hout, ctypes.byref(info)
)
columns = info.srWindow.Right - info.srWindow.Left
rows = info.srWindow.Bottom - info.srWindow.Top + 1
import ipdb; ipdb.set_trace()
