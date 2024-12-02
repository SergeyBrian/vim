from app.editor.command.command import Command
from app.editor.command.text import TextCommand
from app.editor.controllers.text import TextController


class NewLineCommand(TextCommand):
    def __init__(self, text_controller: TextController, wrap: bool):
        super().__init__(text_controller)
        self._wrap = wrap


    def execute(self):
        self._text_controller.new_line(self._wrap)
