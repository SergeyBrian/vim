from mystring import MyString
from enum import Enum
from app.editor.utils.keys import Key
from app.editor.view import debug as dbg_view


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
        self._filename = ""

    def _send_updates(self):
        dbg_view.instance().set("cursor", self._cursor.__dict__)
        for fn in self._subscribers:
            fn()

    def load_file(self, filename: str, lines: list[str]):
        self._filename = filename
        self._cursor.col = 0
        self._cursor.row = 0
        self._lines.clear()
        for line in lines:
            self._lines.append(MyString(line.strip()))
        self._send_updates()

    def insert(self, key):
        self._lines[self._cursor.row].insert(self._cursor.col, key)
        self._cursor.col += 1
        self._prev_col = self._cursor.col
        self._send_updates()

    def _fix_cursor(self):
        if self._cursor.row == 0 and self._cursor.col < 0:
            self._cursor.row = 0
            self._cursor.col = 0
        if (self._cursor.row == len(self._lines) - 1 and
                self._cursor.col >= self._lines[self._cursor.row].length()):
            self._cursor.col = self._lines[self._cursor.row].length() - 1

        if self._cursor.row < 0:
            self._cursor.row = 0
            self._cursor.col = 0
        if self._cursor.row >= len(self._lines):
            self._cursor.row = len(self._lines) - 1
            self._cursor.col = self._lines[self._cursor.row].length() - 1

        if self._cursor.col < 0:
            self._cursor.row -= 1
            self._cursor.col = self._lines[self._cursor.row].length() - 1
        if self._cursor.col >= self._lines[self._cursor.row].length():
            self._cursor.row += 1
            self._cursor.col = 0

    @staticmethod
    def _is_delimiter(c):
        return not c.isalnum()

    def _map_words(self, row: int):
        res = []
        line = self._lines[row]
        start = 0
        for i in range(line.length()):
            if self._is_delimiter(line[i]):
                res.append((start, i - 1))
                start = i + 1
        res.append((start, line.length() - 1))
        return res

    def move_cursor_word(self, forward: bool):
        dir = 1 if forward else -1
        words = self._map_words(self._cursor.row)
        dbg_view.instance().set("words", words)
        cur_word = 0
        for i, w in enumerate(words):
            if w[0] <= self._cursor.col <= w[1]:
                cur_word = i
                break
        dbg_view.instance().set("cur_word", cur_word)

        if (not forward and
                words[cur_word][0] < self._cursor.col):
            new_word = cur_word
        else:
            new_word = cur_word + dir

        if 0 <= new_word < len(words):
            self.set_cursor(self._cursor.row, words[new_word][0])
            return
        else:
            new_row = self._cursor.row + dir
            if new_row < 0:
                return
            if new_row >= len(self._lines):
                return
            new_words = self._map_words(new_row)
            if forward:
                words = [*words, *new_words]
            else:
                new_word += len(new_words)
                words = [*new_words, *words]

            dbg_view.instance().set("words", words)
            self.set_cursor(new_row, words[new_word][0])

    def delete_next(self, forward: bool):
        a = CursorPos(row=self._cursor.row, col=self._cursor.col)
        self.move_cursor_word(forward)
        b = CursorPos(row=self._cursor.row, col=self._cursor.col)
        if a.row < b.row or (a.row == b.row and a.col < b.col):
            start = a
            end = b
        else:
            start = b
            end = a
        self._delete(start, end)

    def _delete(self, start: CursorPos, end: CursorPos):
        dbg_view.instance().set("del_start", start.__dict__)
        dbg_view.instance().set("del_end", end.__dict__)
        if start.row == end.row:
            self._lines[start.row].erase(start.col, end.col - start.col)
        else:
            self._lines[start.row].erase(
                start.col, self._lines[start.row].length() - start.col
            )
            for i in range(start.row, end.row):
                self._lines[i] += self._lines[i + 1]
                del self._lines[i + 1]
            if end.row < len(self._lines):
                self._lines[end.row].erase(0, end.col)
        self.set_cursor(start.row, start.col)

    def delete_word(self):
        cur_line = self._lines[self._cursor.row]
        if cur_line.empty():
            return
        if cur_line[self._cursor.col] == " ":
            self.delete(1)
            return
        start = self._cursor.col
        end = self._cursor.col

        while start > 0 and cur_line[start].isalnum():
            start -= 1
        while end < cur_line.length() and cur_line[end].isalnum():
            end += 1
        self._delete(CursorPos(row=self._cursor.row, col=start),
                     CursorPos(row=self._cursor.row, col=end))

    def delete(self, dir):
        a = CursorPos(
            col=self._cursor.col,
            row=self._cursor.row
        )
        b = CursorPos(
            col=self._cursor.col,
            row=self._cursor.row
        )

        dbg_view.instance().set("dir", dir)
        a.col += dir

        while a.col < 0:
            a.row -= 1
            if a.row < 0:
                a.row = 0
                a.col = 0
                break
            a.col += self._lines[a.row].length() + 1

        while a.col > self._lines[a.row].length():
            a.row += 1
            if a.row > len(self._lines):
                a.row = len(self._lines) - 1
                a.col = self._lines[a.row].length() - 1
                break
            a.col -= self._lines[a.row].length() - 1

        if a.row < b.row or (a.row == b.row and a.col < b.col):
            start = a
            end = b
        else:
            start = b
            end = a

        self._delete(start, end)
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
        cur_line_l = self._lines[self._cursor.row].length()
        if (0 <= self._cursor.col + d and
                (self._cursor.col + d < cur_line_l) or
                (self._mode == Mode.INSERT and
                 self._cursor.col + d == cur_line_l)):
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

    def set_cursor(self, row: int | None, col: int | None):
        if row is not None:
            if row < 0:
                row = len(self._lines)
            self._cursor.row = min(max(0, row), len(self._lines) - 1)
            self._cursor.col = min(
                self._lines[self._cursor.row].length(),
                self._prev_col
            )
        if col is not None:
            if col < 0 or col >= len(self._lines[self._cursor.row]):
                col = len(self._lines[self._cursor.row])
                if self._mode != Mode.INSERT:
                    col -= 1
            self._cursor.col = max(0, col)
        self._send_updates()

    def move_cursor(self, offset: int):
        new_pos = self._cursor_pos + offset
        if new_pos < 0 or new_pos > len(self._input_buffer):
            self._send_updates()
            return
        self._cursor_pos = new_pos

    def get_cursor_pos(self):
        return self._cursor_pos

    def get_cursor(self):
        return self._cursor

    def get_input_buffer(self):
        return self._input_buffer

    def set_input_buffer(self, value: str):
        dbg_view.instance().set("cmd_buf", self._input_buffer)
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
        if mode == Mode.NORMAL:
            self.move_cursor_h(-1)
        self._send_updates()

    def register_subscriber(self, subscriber):
        self._subscribers.append(subscriber)
