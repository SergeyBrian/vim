from app.editor.command.command import Command
from app.editor.command.text import TextCommand
from app.editor.controllers.text import TextController


class DeleteLineCommand(TextCommand):
    def execute(self):
        self._text_controller.delete_line()
