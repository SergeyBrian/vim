from app.editor.command.command import Command
from app.editor.controller.interface import ControllerInterface
from app.editor.model.interface import TextModel


class NewLineCommand(Command):
    def __init__(self,
                 controller: ControllerInterface,
                 model: TextModel,
                 wrap: bool,
                 above: bool):
        super().__init__(controller, model)
        self._wrap = wrap
        self._above = above

    def execute(self):
        self._model.new_line(self._wrap, above=self._above)
        self._controller.set_state(self._controller.insert_mode)
