from mystring import MyString


class CursorPos:
    def __init__(self, col: int, row: int):
        self.col: int = col
        self.row: int = row


class TextModel:
    def __init__(self):
        self._lines: list[MyString] = [MyString()]
        self._cursor: CursorPos = CursorPos(0, 0)

    def insert(self, key):
        self._lines[self._cursor.row].insert(self._cursor.col, key)
        self._cursor.col += 1

    def get_lines(self):
        return self._lines

    def get_cursor(self):
        return self._cursor

    def delete_line(self):
        if len(self._lines) == 1:
            self._lines[0] = MyString("")
            self._cursor.row = 0
            self._cursor.col = 0
            return
        self._lines.pop(self._cursor.row)
        self._cursor.row -= 1
        if self._cursor.row < 0:
            self._cursor.row = 0
        self._cursor.col = min(
            self._cursor.col,
            self._lines[self._cursor.row].length() - 1
        )

    def new_line(self, wrap: bool, above=False):
        cur_line = self._lines[self._cursor.row]
        offset = 0 if above else 1
        if not wrap or self._cursor.col == cur_line.length():
            self._cursor.row += offset
            self._lines.insert(self._cursor.row, MyString(""))
            self._cursor.col = 0
            return
        new_str = cur_line.substr(self._cursor.col)
        cur_line.erase(self._cursor.col, new_str.length())
        self._cursor.row += offset
        self._lines.insert(self._cursor.row, new_str)
        self._cursor.col = 0

        

    def cursor_forward(self, d: int):
        if 0 <= self._cursor.col + d < self._lines[self._cursor.row].length():
            self._cursor.col += d

