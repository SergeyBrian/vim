from abc import ABC, abstractmethod

from app.editor.command.command import Command
from app.editor.command.factory import CmdTree, CommandFactory
from app.editor.model.model import Mode
from app.editor.utils.keys import Key
from app.editor.controller.interface import ControllerInterface


class BaseState(ABC):
    def __init__(self, cmd_factory: CommandFactory):
        self._cmd_factory: CommandFactory = cmd_factory
        self.mode = None

    @abstractmethod
    def handle_key(
        self,
        command_controller: ControllerInterface,
        prev_cmd: CmdTree | None,
        cmd_buf: str,
        key: Key | str,
    ):
        raise NotImplementedError

    def pre_handle(self, controller: ControllerInterface, key: Key | str):
        if isinstance(key, Key) and key is Key.KEY_ESC:
            controller.set_state(NormalState(self._cmd_factory))
            return False
        return True

    def post_handle(
        self, cmd: Command | CmdTree, need_reset: bool
    ) -> tuple[CmdTree | None, bool]:
        if not cmd:
            return None, need_reset
        if isinstance(cmd, Command):
            cmd.execute()
            return None, True
        return cmd, need_reset


class NormalState(BaseState):
    def __init__(self, cmd_factory: CommandFactory):
        super().__init__(cmd_factory)
        self.mode = Mode.NORMAL

    def handle_key(
        self,
        command_controller: ControllerInterface,
        prev_cmd: CmdTree | None,
        cmd_buf: str,
        key: Key | str,
    ) -> tuple[CmdTree | None, bool, bool]:
        if not super().pre_handle(command_controller, key):
            return None, True, False

        if prev_cmd is None and not cmd_buf:
            if key == "i":
                command_controller.set_state(InsertState(self._cmd_factory))
                return None, True, True
            elif key == Key.KEY_BACKSPACE or key == Key.KEY_LEFT:
                key = "h"
            elif key == "\n" or key == Key.KEY_DOWN:
                key = "j"
            elif key == Key.KEY_RIGHT:
                key = "l"
            elif key == Key.KEY_UP:
                key = "k"

        command, need_reset, found = self._cmd_factory.build_command(
            prev_cmd, cmd_buf, key)

        return *super().post_handle(command, need_reset), found


class InsertState(BaseState):
    def __init__(self, cmd_factory: CommandFactory):
        super().__init__(cmd_factory)
        self.mode = Mode.INSERT

    def handle_key(
        self,
        command_controller: ControllerInterface,
        prev_cmd: CmdTree | None,
        cmd_buf: str,
        key: Key | str,
    ):
        if not super().pre_handle(command_controller, key):
            return None, True, True
        # TODO: fix this..
        if key == "\n":
            cmd = self._cmd_factory.build_new_line_command(wrap=True)
        elif key == Key.KEY_BACKSPACE:
            cmd = self._cmd_factory.build_delete_command(-1)
        elif key in [Key.KEY_DOWN, Key.KEY_UP, Key.KEY_LEFT, Key.KEY_RIGHT]:
            if key == Key.KEY_LEFT:
                key = "h"
            elif key == Key.KEY_DOWN:
                key = "j"
            elif key == Key.KEY_RIGHT:
                key = "l"
            elif key == Key.KEY_UP:
                key = "k"
            cmd, _, _ = self._cmd_factory.build_command(
                None, "", key)

        else:
            cmd = self._cmd_factory.build_insert_command(key)
        return *super().post_handle(cmd, True), True
