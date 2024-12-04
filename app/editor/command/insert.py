from app.editor.command.command import Command
from app.editor.controller.interface import ControllerInterface
from app.editor.model.interface import TextModel


class InsertCommand(Command):
    def __init__(self, controller: ControllerInterface, model: TextModel, key: str):
        super().__init__(controller, model)
        self._key = key

    def execute(self):
        self._model.insert(self._key)
