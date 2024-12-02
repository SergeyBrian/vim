from app.editor.models.text import TextModel
from app.editor.view.text import TextView


class TextController:
    def __init__(self, model: TextModel, view: TextView):
        self._model = model
        self._view = view

    def insert(self, key: str):
        self._model.insert(key)

    def delete_line(self):
        self._model.delete_line()

    def new_line(self, wrap: bool):
        self._model.new_line(wrap)

    def cursor_forward(self, d: int):
        self._model.cursor_forward(d)
