from mystring import MyString
from enum import Enum
from app.editor.utils.keys import Key


class CursorPos:
    def __init__(self, col: int, row: int):
        self.col: int = col
        self.row: int = row

    def get(self):
        return (self.col, self.row)


class Mode(Enum):
    NORMAL = 1
    INSERT = 2
    COMMAND = 3


class Model:
    def __init__(self):
        self._lines: list[MyString] = [MyString()]
        self._cursor: CursorPos = CursorPos(0, 0)
        self._prev_col: int = 0
        self._mode = Mode.NORMAL
        self._input_buffer = ""
        self._cursor_pos = 0
        self._subscribers = []

    def _send_updates(self):
        for fn in self._subscribers:
            fn()

    def insert(self, key):
        self._lines[self._cursor.row].insert(self._cursor.col, key)
        self._cursor.col += 1
        self._prev_col = self._cursor.col
        self._send_updates()

    def delete_line(self):
        if len(self._lines) == 1:
            self._lines[0] = MyString("")
            self._cursor.row = 0
            self._cursor.col = 0
            self._send_updates()
            return
        self._lines.pop(self._cursor.row)
        self._cursor.row -= 1
        if self._cursor.row < 0:
            self._cursor.row = 0
        self._cursor.col = min(
            self._cursor.col, self._lines[self._cursor.row].length() - 1
        )
        self._send_updates()

    def new_line(self, wrap: bool, above=False):
        cur_line = self._lines[self._cursor.row]
        offset = 0 if above else 1
        if not wrap or self._cursor.col == cur_line.length():
            self._cursor.row += offset
            self._lines.insert(self._cursor.row, MyString(""))
            self._cursor.col = 0
            self._send_updates()
            return
        new_str = cur_line.substr(self._cursor.col)
        cur_line.erase(self._cursor.col, new_str.length())
        self._cursor.row += offset
        self._lines.insert(self._cursor.row, new_str)
        self._cursor.col = 0

    def get_lines(self):
        return [line.c_str() for line in self._lines]

    def move_cursor_h(self, d: int):
        if 0 <= self._cursor.col + d < self._lines[self._cursor.row].length():
            self._cursor.col += d
            self._prev_col = self._cursor.col
            self._send_updates()

    def move_cursor_v(self, d: int):
        if 0 <= self._cursor.row + d < len(self._lines):
            self._cursor.row += d
            self._cursor.col = min(
                self._lines[self._cursor.row].length(),
                self._prev_col
            )
            self._send_updates()

    def move_cursor(self, offset: int):
        new_pos = self._cursor_pos + offset
        if new_pos < 0 or new_pos > len(self._input_buffer):
            self._send_updates()
            return
        self._cursor_pos = new_pos

    def get_cursor_pos(self):
        return self._cursor_pos

    def get_text_cursor(self):
        return self._cursor

    def get_input_buffer(self):
        return self._input_buffer

    def set_input_buffer(self, value: str):
        self._input_buffer = value
        self._cursor_pos = len(value)
        self._send_updates()

    def push_input_buffer(self, ch: Key | str):
        if ch == Key.KEY_ENTER:
            self._input_buffer += ch
            self._cursor_pos = len(self._input_buffer)
            self._send_updates()
            return
        elif ch == Key.KEY_LEFT:
            new_pos = self._cursor_pos - 1
            if new_pos >= 0:
                self._cursor_pos = new_pos
                self._send_updates()
                return
        elif ch == Key.KEY_RIGHT:
            new_pos = self._cursor_pos + 1
            if new_pos <= len(self._input_buffer):
                self._cursor_pos = new_pos
                self._send_updates()
                return
        elif ch == Key.KEY_BACKSPACE:
            self._input_buffer = (
                self._input_buffer[: self._cursor_pos - 1]
                + self._input_buffer[self._cursor_pos:]
            )
            self._cursor_pos -= 1
            self._send_updates()
            return
        elif ch == Key.KEY_DELETE:
            self._input_buffer = (
                self._input_buffer[: self._cursor_pos]
                + self._input_buffer[self._cursor_pos + 1:]
            )
            self._send_updates()
            return

        if not isinstance(ch, str) or ch == "":
            self._send_updates()
            return

        idx = self._cursor_pos
        self._input_buffer = (
            self._input_buffer[:idx] + ch + self._input_buffer[idx:]
        )
        self._cursor_pos += 1
        self._send_updates()

    def get_mode(self):
        return self._mode

    def set_mode(self, mode):
        self._mode = mode
        self._send_updates()

    def register_subscriber(self, subscriber):
        self._subscribers.append(subscriber)
