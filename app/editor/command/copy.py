from app.editor.command.command import Command
from app.editor.controller.interface import ControllerInterface
from app.editor.model.interface import TextModel


class CopyLineCommand(Command):
    def __init__(self, controller: ControllerInterface, model: TextModel, line: bool):
        super().__init__(controller, model)
        self._line = line

    def execute(self):
        self._model.copy_line(self._line)


class PasteCommand(Command):
    def execute(self):
        self._model.paste()
