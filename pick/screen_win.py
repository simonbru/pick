import msvcrt
import sys

class Screen:

    def __init__(self):
        self.buffer = []

    @staticmethod
    def clear():
        print('\x1b[2J\x1b[H', end='')

    def refresh(self):
        self.clear()
        for line in self.buffer:
            if type(line) is tuple:
                print(line[0])
            else:
                print(line)
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
