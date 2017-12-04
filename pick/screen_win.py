import ctypes
import ctypes.wintypes
import msvcrt
import sys
from itertools import islice


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


class Screen:
    def __init__(self):
        self.buffer = []

    @staticmethod
    def clear():
        print('\x1b[2J\x1b[H', end='')

    def refresh(self):
        self.clear()
        rows = self.rows
        columns = self.columns
        lines = []
        for line in islice(self.buffer, rows):
            if type(line) is tuple:
                lines.append(line[0][:columns])
            else:
                lines.append(line[:columns])
        print(*lines, sep='\n', end='')
        self.buffer = []

    def add_line(self, line):
        self.buffer.append(line)

    @staticmethod
    def getch():
        char = msvcrt.getch()
        if char in (b'\x00', b'\xe0'):
            char += msvcrt.getch()
            return char
        else:
            return ord(char)

    @staticmethod
    def _screen_info():
        hout = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        info = CONSOLE_SCREEN_BUFFER_INFO()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(
            hout, ctypes.byref(info)
        )
        return info

    @property
    def rows(self):
        info = self._screen_info()
        return info.srWindow.Bottom - info.srWindow.Top + 1

    @property
    def columns(self):
        info = self._screen_info()
        return info.srWindow.Right - info.srWindow.Left
