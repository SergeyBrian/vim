
from app.editor.command.command import Command
from app.editor.controller.interface import ControllerInterface
from app.editor.model.interface import TextModel


class DeleteCommand(Command):
    def __init__(self, controller: ControllerInterface, model: TextModel, d: int):
        super().__init__(controller, model)
        self._dir = d

    def execute(self):
        self._model.delete(self._dir)


class DeleteWordCommand(Command):
    def execute(self):
        self._model.delete_word()


class DeleteNextCommand(Command):
    def __init__(self,
                 controller: ControllerInterface,
                 model: TextModel,
                 forward: bool):
        super().__init__(controller, model)
        self._forward = forward

    def execute(self):
        self._model.delete_next(self._forward)
