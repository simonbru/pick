import msvcrt
import shutil
import sys
from itertools import islice


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

    @property
    def rows(self):
        return shutil.get_terminal_size().lines

    @property
    def columns(self):
        return shutil.get_terminal_size().columns - 1
