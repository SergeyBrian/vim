import curses

from app.editor.utils.keys import Key
from app.ui.render import BaseRenderer, Drawable, Text, Window, Cursor


class CursesWindow:
    def __init__(self, win: curses.window):
        self.delete = False
        self.window = win


class CursesRenderer(BaseRenderer):
    def __init__(self):
        super().__init__()
        self._screen = None
        self._windows: dict[Window, CursesWindow] = {}

    def init(self):
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.set_escdelay(25)
        curses.curs_set(True)
        self._screen.keypad(True)

    def shutdown(self):
        curses.nocbreak()
        curses.echo()
        self._screen.keypad(False)
        curses.endwin()

    @staticmethod
    def curses_ch_to_key(ch: int) -> Key | str:
        if ch in Key:
            return Key(ch)
        return chr(ch)

    def getch(self) -> Key | str:
        return self.curses_ch_to_key(self._screen.getch())

    def render(self):
        self._screen.clear()
        for window in self._windows.values():
            window.delete = True

        for obj in self._draw_calls:
            self._draw(obj)
        self._draw_calls.clear()
        windows_to_delete = [key for key, win in self._windows.items() if win.delete]
        for window in windows_to_delete:
            self._windows.pop(window)

    def _draw(self, obj: Drawable, window=None):
        if not window:
            window = self._screen

        obj.resolve_geometry(*window.getmaxyx())

        if isinstance(obj, Text):
            window.addstr(obj.y, obj.x, obj.text)
        elif isinstance(obj, Window):
            if obj not in self._windows:
                self._windows[obj] = CursesWindow(window.subwin(obj.h, obj.w, obj.y, obj.x))

            win = self._windows[obj]
            win.delete = False
            for item in obj.items:
                self._draw(item, win.window)
            win.window.refresh()
        elif isinstance(obj, Cursor):
            y, x = window.getbegyx()
            self._screen.move(y + obj.y, x + obj.x)

    def _clear(self, obj: Drawable):
        y, x = curses.getsyx()
        self._screen.move(obj.y, obj.x)
        self._screen.clrtoeol()
        self._screen.move(y, x)
