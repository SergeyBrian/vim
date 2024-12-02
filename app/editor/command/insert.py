from app.editor.command.command import Command
from app.editor.command.text import TextCommand
from app.editor.controllers.text import TextController


class InsertCommand(TextCommand):
    def __init__(self, text_controller: TextController, key: str):
        super().__init__(text_controller)
        self._key = key

    def execute(self):
        self._text_controller.insert(self._key)
