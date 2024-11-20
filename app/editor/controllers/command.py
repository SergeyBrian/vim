from app.editor.command.command import InvalidCommandException
from app.editor.command.factory import CommandFactory
from app.editor.controllers.editor_interface import EditorControllerInterface
from app.editor.controllers.text import TextController
from app.editor.models.command import CommandModel
from app.editor.utils.keys import Key
from app.editor.view.command import CommandView


class CommandController:
    def __init__(self,
                 model: CommandModel,
                 view: CommandView,
                 text_controller: TextController):
        self._model = model
        self._view = view
        self._text_controller = text_controller
        self._editor_controller = None
        self._command_factory = None

    def set_editor_controller(self, editor_controller: EditorControllerInterface):
        self._editor_controller = editor_controller
        self._command_factory = CommandFactory(editor_controller, self._text_controller)

    def handle_key(self, key: Key | str):
        if key == Key.KEY_ESC:
            self._model.set_input_buffer("")
        else:
            self._model.push_input_buffer(key)
        try:
            cmd = self._command_factory.build_command(self._model.get_input_buffer())
            if not cmd:
                return
            else:
                cmd.execute()
            self._model.set_input_buffer("")
        except InvalidCommandException:
            self._model.set_input_buffer("")
        finally:
            self._view.update_cmd(self._model.get_input_buffer())
            self._view.set_cursor(self._model.get_cursor_pos())

