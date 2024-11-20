from app.editor.models.text import TextModel
from app.editor.view.text import TextView


class TextController:
    def __init__(self, model: TextModel, view: TextView):
        self._model = model
        self._view = view

    def process_key(self, key: int):
        pass
