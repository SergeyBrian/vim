from enum import Enum

from app.editor.utils.keys import Key


class Mode(Enum):
    NORMAL = 1
    INSERT = 2
    COMMAND = 3


class CommandModel:
    def __init__(self):
        self._mode = Mode.NORMAL
        self._input_buffer = ""
        self._cursor_pos = 0

    def move_cursor(self, offset: int):
        new_pos = self._cursor_pos + offset
        if new_pos < 0 or new_pos > len(self._input_buffer):
            return
        self._cursor_pos = new_pos

    def get_cursor_pos(self):
        return self._cursor_pos

    def get_input_buffer(self):
        return self._input_buffer

    def set_input_buffer(self, value: str):
        self._input_buffer = value
        self._cursor_pos = len(value)

    def push_input_buffer(self, ch: Key | str):
        if ch == Key.KEY_ENTER:
            self._input_buffer += ch
            self._cursor_pos = len(self._input_buffer)
            return
        elif ch == Key.KEY_LEFT:
            new_pos = self._cursor_pos - 1
            if new_pos >= 0:
                self._cursor_pos = new_pos
                return
        elif ch == Key.KEY_RIGHT:
            new_pos = self._cursor_pos + 1
            if new_pos <= len(self._input_buffer):
                self._cursor_pos = new_pos
                return
        elif ch == Key.KEY_BACKSPACE:
            self._input_buffer = self._input_buffer[:self._cursor_pos - 1] + self._input_buffer[self._cursor_pos:]
            self._cursor_pos -= 1
            return
        elif ch == Key.KEY_DELETE:
            self._input_buffer = self._input_buffer[:self._cursor_pos] + self._input_buffer[self._cursor_pos + 1:]
            return

        if not isinstance(ch, str) or ch == "":
            return

        idx = self._cursor_pos
        self._input_buffer = self._input_buffer[:idx] + ch + self._input_buffer[idx:]
        self._cursor_pos += 1

    def get_mode(self):
        return self._mode

    def set_mode(self, mode):
        self._mode = mode
