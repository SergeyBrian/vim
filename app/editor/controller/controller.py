from app.ui.adapter import Adapter
from app.editor.model.model import Model
from app.editor.view.view import View
from app.editor.utils.keys import Key
from app.editor.command.command import InvalidCommandException
from app.editor.command.factory import CmdTree, CommandFactory
from app.editor.command.state import BaseState, NormalState, InsertState
from app.editor.view import debug as dbg_view


class Controller:
    def __init__(self, renderer: Adapter):
        self._model = Model()
        self._view = View(renderer)

        dbg_view.init(renderer)

        self._running = True
        self._renderer = renderer
        self._cur_cmd: CmdTree | None = None
        cmd_factory = CommandFactory(self, self._model)
        self.normal_mode = NormalState(cmd_factory)
        self.insert_mode = InsertState(cmd_factory)
        self._state: BaseState = self.normal_mode
        self._arg_buf = ""
        self._allow_insert = True

    def handle_key(self, key: Key | str):
        try:
            next_cmd, need_reset, found = self._state.handle_key(
                self, self._cur_cmd, self._arg_buf, key
            )
            if not next_cmd:
                self._reset_cmd()
                self._arg_buf = ""
            else:
                dbg_view.instance().set("arg_buf", self._arg_buf)
                # dbg_view.instance().set("next_cmd", next_cmd)
                # dbg_view.instance().set("cur_cmd", self._cur_cmd)
                if not need_reset:
                    if not found:
                        if isinstance(key, str):
                            self._arg_buf += key
                        elif key is Key.KEY_BACKSPACE:
                            self._arg_buf = self._arg_buf[:-1]
                        dbg_view.instance().set("arg_buf", self._arg_buf)
                    self._model.push_input_buffer(key)
                self._cur_cmd = next_cmd

        except InvalidCommandException:
            self._reset_cmd()

    def _reset_cmd(self):
        self._model.set_input_buffer("")
        self._cur_cmd = None

    def open_file(self, filename: str):
        with open(filename, "r") as file:
            self.set_state(self.normal_mode)
            lines = file.readlines()
            self._model.load_file(filename, lines)

    def save_file(self, filename: str):
        if not filename:
            filename = self._model._filename
        with open(filename, "w") as file:
            for line in self._model.get_lines():
                file.write(f"{line.c_str()}\n")

    def set_state(self, state: BaseState):
        if not self._allow_insert:
            state = self.normal_mode
        self._state = state
        self._reset_cmd()
        self._model.set_mode(state.mode)

    def run(self, init_file: str = "", allow_insert: bool = True):
        self._allow_insert = allow_insert
        try:
            need_init = self._renderer.need_init()
            if need_init:
                self._renderer.init()
            self._view.observe(self._model)
            if init_file:
                self.open_file(init_file)
            ch: Key | str = ""
            while True:
                self.handle_key(ch)
                if not self._running:
                    break
                ch = self._renderer.getch()
        except KeyboardInterrupt:
            pass
        finally:
            if need_init:
                self._renderer.shutdown()

    def help(self):
        r = self._renderer.split_v()
        help_c = Controller(r)
        help_c.run(init_file="help.txt", allow_insert=False)

    def quit(self):
        self._running = False
