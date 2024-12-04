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

    def pre_handle(self, command_controller: ControllerInterface, key: Key | str):
        if isinstance(key, Key) and key is Key.KEY_ESC:
            command_controller.set_state(NormalState(self._cmd_factory))
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
    ) -> tuple[CmdTree | None, bool]:
        if not super().pre_handle(command_controller, key):
            return None, True

        if prev_cmd is None and not cmd_buf:
            if key == "i":
                command_controller.set_state(InsertState(self._cmd_factory))
                return None, True

        command, need_reset = self._cmd_factory.build_command(
            prev_cmd, cmd_buf, key)

        return super().post_handle(command, need_reset)


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
            return None, True
        # TODO: fix this..
        if key == "\n":
            cmd = self._cmd_factory.build_new_line_command(wrap=True)
        else:
            cmd = self._cmd_factory.build_insert_command(key)
        return super().post_handle(cmd, True)
