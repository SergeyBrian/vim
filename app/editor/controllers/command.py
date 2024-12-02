from app.editor.command.command import InvalidCommandException
from app.editor.command.factory import CommandFactory, CmdTree
from app.editor.command.state import BaseState, NormalState
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
        self._cur_cmd: CmdTree | None = None
        self._state: BaseState | None = None

    def set_editor_controller(self, editor_controller: EditorControllerInterface):
        self._editor_controller = editor_controller
        self._command_factory = CommandFactory(editor_controller, self._text_controller)
        self._state: BaseState = NormalState(self._command_factory)

    def handle_key(self, key: Key | str):
        try:
            next_cmd, need_reset = self._state.handle_key(
                self,
                self._cur_cmd,
                self._model.get_input_buffer(),
                key
            )
            if not next_cmd:
                self._reset_cmd()
            else:
                self._cur_cmd = next_cmd
                if not need_reset:
                    self._model.push_input_buffer(key)

        except InvalidCommandException:
            self._reset_cmd()
        finally:
            self._view.render()

    def set_state(self, state: BaseState):
        self._state = state
        self._reset_cmd()
        self._model.set_mode(state.mode)

    def _reset_cmd(self):
        self._model.set_input_buffer("")
        self._cur_cmd = None
