from app.editor.command.command import Command
from app.editor.controller.interface import ControllerInterface
from app.editor.model.interface import TextModel


class MoveCursorCommand(Command):
    def __init__(self,
                 controller: ControllerInterface,
                 model: TextModel,
                 d: int,
                 vertical: bool):
        super().__init__(controller, model)
        self._dir = d
        self._vertical = vertical

    def execute(self):
        if self._vertical:
            self._model.move_cursor_v(self._dir)
        else:
            self._model.move_cursor_h(self._dir)
