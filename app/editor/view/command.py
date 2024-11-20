from app.editor.view.base import BaseView
from app.ui.render import BaseRenderer, Text, Window, Alignment, Cursor, CursorVariant


class CommandView(BaseView):
    def __init__(self, renderer: BaseRenderer):
        super().__init__(renderer)
        self._cmd = ""
        self._cursor_pos = 0

    def render(self):
        items = [
            Text(0, 0, self._cmd),
            Text(0, 1, str(self._cursor_pos))
        ]

        if self._cmd != "":
            items.append(Cursor(x=self._cursor_pos, y=0))

        self._renderer.add(
            Window(h=3, w=1.0, items=items, alignment=Alignment.Bottom)
        )

    def update_cmd(self, cmd: str):
        self._cmd = cmd

    def set_cursor(self, pos: int):
        self._cursor_pos = pos
