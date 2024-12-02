from app.editor.command.command import Command
from app.editor.command.text import TextCommand
from app.editor.controllers.text import TextController


class MoveCursorCommand(TextCommand):
    def __init__(self, text_controller: TextController, d: int):
        super().__init__(text_controller)
        self._dir = d

    def execute(self):
        self._text_controller.cursor_forward(self._dir)
