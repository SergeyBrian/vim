from app.ui.render import BaseRenderer
from app.editor.model.model import Model
from app.editor.view.view import View
from app.editor.utils.keys import Key
from app.editor.command.command import InvalidCommandException
from app.editor.command.factory import CmdTree, CommandFactory
from app.editor.command.state import BaseState, NormalState, InsertState


class Controller:
    def __init__(self, renderer: BaseRenderer):
        self._model = Model()
        self._view = View(renderer)

        self._running = True
        self._renderer = renderer
        self._cur_cmd: CmdTree | None = None
        cmd_factory = CommandFactory(self, self._model)
        self.normal_mode = NormalState(cmd_factory)
        self.insert_mode = InsertState(cmd_factory)
        self._state: BaseState = self.normal_mode

    def handle_key(self, key: Key | str):
        try:
            next_cmd, need_reset = self._state.handle_key(
                self, self._cur_cmd, self._model.get_input_buffer(), key
            )
            if not next_cmd:
                self._reset_cmd()
            else:
                self._cur_cmd = next_cmd
                if not need_reset:
                    self._model.push_input_buffer(key)

        except InvalidCommandException:
            self._reset_cmd()

    def _reset_cmd(self):
        self._model.set_input_buffer("")
        self._cur_cmd = None

    def set_state(self, state: BaseState):
        self._state = state
        self._reset_cmd()
        self._model.set_mode(state.mode)

    def run(self):
        try:
            self._renderer.init()
            self._view.observe(self._model)
            ch = ""
            while True:
                self.handle_key(ch)
                if not self._running:
                    break
                ch = self._renderer.getch()
        except KeyboardInterrupt:
            pass
        finally:
            self._renderer.shutdown()

    def quit(self):
        self._running = False
