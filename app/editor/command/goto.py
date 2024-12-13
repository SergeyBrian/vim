from app.editor.command.command import Command
from app.editor.controller.interface import ControllerInterface
from app.editor.model.interface import TextModel
from app.editor.view import debug as dbg_view


class GoToLineCommand(Command):
    def __init__(self,
                 controller: ControllerInterface,
                 model: TextModel,
                 line: int = 0):
        super().__init__(controller, model)
        self._line = line
        # dbg_view.instance().set("goto", self._line)

    def set_arg(self, val):
        self._line = int(val) - 1

    def execute(self):
        self._model.set_cursor(row=self._line, col=None)


class GoToIndexCommand(Command):
    def __init__(self,
                 controller: ControllerInterface,
                 model: TextModel,
                 idx: int,
                 insert: bool = False):
        super().__init__(controller, model)
        self._idx = idx
        self._do_insert = insert

    def execute(self):
        if self._do_insert:
            self._controller.set_state(self._controller.insert_mode)
        self._model.set_cursor(row=None, col=self._idx)
