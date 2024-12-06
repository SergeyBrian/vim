from app.editor.command.command import Command
from app.editor.controller.interface import ControllerInterface
from app.editor.model.interface import TextModel


class MoveCursorCommand(Command):
    def __init__(self,
                 controller: ControllerInterface,
                 model: TextModel,
                 d: int,
                 vertical: bool,
                 insert: bool = False):
        super().__init__(controller, model)
        self._dir = d
        self._vertical = vertical
        self._insert = insert
        self._count = 1

    def set_arg(self, arg):
        self._count = int(arg)

    def execute(self):
        if self._insert:
            self._controller.set_state(self._controller.insert_mode)
        for i in range(self._count):
            if self._vertical:
                self._model.move_cursor_v(self._dir)
            else:
                self._model.move_cursor_h(self._dir)


class MoveCursorWordCommand(Command):
    def __init__(self,
                 controller: ControllerInterface,
                 model: TextModel,
                 forward: bool):
        super().__init__(controller, model)
        self._forward = forward

    def execute(self):
        self._model.move_cursor_word(self._forward)
