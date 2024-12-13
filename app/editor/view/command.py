from app.editor.models.command import CommandModel, Mode
from app.editor.view.base import BaseView
from app.ui.render import IAdapterRenderer, Text, Window, Alignment, Cursor


class CommandView(BaseView):
    def __init__(self, renderer: IAdapterRenderer, model: CommandModel):
        super().__init__(renderer)
        self._model = model

    def render(self):
        items = []
        if self._mode == Mode.INSERT:
            items = [
                Text(0, 0, "-- INSERT --")
            ]
        elif self._mode == Mode.NORMAL:
            items = [
                Text(0, 0, self._cmd),
                Text(0, 1, str(self._cursor_pos))
            ]

            if self._cmd != "":
                items.append(Cursor(x=self._cursor_pos, y=0))

        self._renderer.add(
            Window(h=3, w=1.0, items=items, alignment=Alignment.Bottom)
        )

    @property
    def _cursor_pos(self):
        return self._model.get_cursor_pos()

    @property
    def _cmd(self):
        return self._model.get_input_buffer()

    @property
    def _mode(self):
        return self._model.get_mode()
