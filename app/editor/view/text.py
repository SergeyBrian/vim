from app.editor.models.text import TextModel
from app.editor.view.base import BaseView
from app.ui.render import Text, Window, BaseRenderer, Cursor


class TextView(BaseView):
    def __init__(self, renderer: BaseRenderer, model: TextModel):
        super().__init__(renderer)
        self._model = model

    def render(self):
        items = list([
            Text(0, y, f"{line.c_str()}")
            for y, line in enumerate(self._text)
        ])
        items.append(Cursor(x=self._cursor.col, y=self._cursor.row))
        self._renderer.add(
            Window(0.9, 1.0, items=items)
        )

    @property
    def _text(self):
        return self._model.get_lines()

    @property
    def _cursor(self):
        return self._model.get_cursor()
