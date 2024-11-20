from app.editor.command.command import InvalidCommandException
from app.editor.command.factory import CommandFactory
from app.editor.controllers.command import CommandController
from app.editor.controllers.text import TextController
from app.editor.models.editor import EditorModel
from app.editor.utils.keys import Key
from app.editor.view.editor import EditorView
from app.ui.render import Text


class EditorController:
    def __init__(self,
                 model: EditorModel,
                 view: EditorView,
                 command_controller: CommandController):
        self._model = model
        self._view = view
        self._command_controller = command_controller
        self._command_controller.set_editor_controller(self)

    def process_key(self, key: Key | str):
        self._command_controller.handle_key(key)
        self._view.render()

    def quit(self):
        self._model.set_running(False)

    def running(self):
        return self._model.running()
