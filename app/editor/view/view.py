from app.ui.render import IAdapterRenderer, Text, Window, Cursor, Alignment, Drawable
from app.editor.model.model import Model, Mode, CursorPos
from app.editor.model.observable import Observable
from app.editor.utils.consts import CMD_SYMBOLS
from app.editor.view import debug as dbg_view


class View:
    def __init__(self, renderer: IAdapterRenderer):
        self._renderer = renderer

        self._cmd_offset = 0

        self._model: Model

        self._cur_text_offset_v = 0
        self._cur_text_offset_h = 0

    def observe(self, model: Observable):
        model.register_subscriber(self._on_update)
        self._model = model

    @property
    def _cur_mode(self):
        return self._model.get_mode()

    @property
    def _cmd_buf(self):
        return self._model.get_input_buffer()

    @property
    def _cmd_cursor_idx(self):
        return self._model.get_cursor_pos()

    @property
    def _visible_lines(self):
        lines = self._model.get_lines()
        # return lines[self._cur_text_offset_v:self._renderer.get_height() - 3]
        offset = self._cur_text_offset_v
        limit = self._renderer.get_height() - 2
        return map(lambda x: x.c_str(), lines[offset:(limit + offset if limit is not None else None)])

    @property
    def _cursor(self):
        curs = self._model.get_cursor()
        return CursorPos(curs.col, curs.row - self._cur_text_offset_v)

    def _render(self):
        items: list[Drawable] = list([
            Text(0, y, f"{line}")
            for y, line in enumerate(self._visible_lines)
        ])
        items.append(
            Cursor(x=self._cursor.col, y=self._cursor.row)
        )
        self._renderer.add(
            Window(self._renderer.get_height() - 2, 1.0, items=items)
        )

        if self._cur_mode == Mode.INSERT:
            items = [
                Text(0, 1, "-- INSERT --"),
            ]
        elif self._cur_mode == Mode.NORMAL:
            alignment = Alignment.Left
            if (self._cmd_buf and self._cmd_buf[0] not in CMD_SYMBOLS):
                alignment = Alignment.Right
            items = [
                Text(0, 1, self._cmd_buf, alignment),
            ]

            if self._cmd_buf != "" and self._cmd_buf[0] in CMD_SYMBOLS:
                items.append(Cursor(x=self._cmd_cursor_idx, y=1))

        curs_info = f"{self._model.get_cursor().row + 1}:{
            self._model.get_cursor().col + 1}"
        items.append(
            Text(0, 0, curs_info, alignment=Alignment.Right)
        )
        if self._model._filename:
            items.append(
                Text(0, 0, self._model._filename)
            )
        self._renderer.add(
            Window(h=2, w=1.0, items=items, alignment=Alignment.Bottom)
        )

        self._renderer.render()

    @property
    def _height(self):
        return self._renderer.get_height() - 3

    def _on_update(self):
        cursor = self._model.get_cursor()
        while cursor.row - self._cur_text_offset_v > self._height:
            self._cur_text_offset_v += 1
        while cursor.row - self._cur_text_offset_v < 0:
            self._cur_text_offset_v -= 1
        dbg_view.instance().set("offset", self._cur_text_offset_v)

        self._render()
