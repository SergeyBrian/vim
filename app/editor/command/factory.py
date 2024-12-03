import cmd
import dataclasses
from enum import Enum

from app.editor.command.command import Command, InvalidCommandException
from app.editor.command.cursor import MoveCursorCommand
from app.editor.command.delete_line import DeleteLineCommand
from app.editor.command.insert import InsertCommand
from app.editor.command.new_line import NewLineCommand
from app.editor.command.quit import QuitCommand
from app.editor.controllers.editor_interface import EditorControllerInterface
from app.editor.controllers.text import TextController
from app.editor.utils.keys import Key


class Expect(Enum):
    Number = 1
    Char = 1 << 1
    Empty = 1 << 2
    Any = 1 << 3

    @classmethod
    def validate(cls, e: int, s: str) -> bool:
        if e & cls.Any.value:
            return True
        if e & cls.Number.value and s.isnumeric():
            return True
        if e & cls.Char.value and s.isalpha() and len(s) == 1:
            return True
        if e & cls.Empty.value and len(s) == 0:
            return True
        return False


@dataclasses.dataclass
class CmdTree:
    cmd: Command | None
    children: dict | None
    expect: int

    def get(self, key: Key | str):
        if isinstance(key, Key) and key is Key.KEY_ESC:
            raise Exception(
                "Escape key reached command factory. This should never happen!"
            )

        node: CmdTree | None = self.children.get(key, None)
        if node is None:
            return self

        if node.children is None:
            return node.cmd
        return node


class CommandFactory:
    def __init__(
        self,
        editor_controller: EditorControllerInterface,
        text_controller: TextController,
    ):
        self._editor_controller = editor_controller
        self._text_controller = text_controller

        self._commands: CmdTree = CmdTree(
            cmd=None,
            expect=Expect.Number.value | Expect.Empty.value,
            children={
                ":": CmdTree(
                    cmd=None,
                    expect=Expect.Any.value,
                    children={
                        "q": CmdTree(
                            cmd=None,
                            expect=Expect.Any.value,
                            children={
                                "\n": CmdTree(
                                    QuitCommand(self._editor_controller),
                                    children=None,
                                    expect=Expect.Any.value,
                                ),
                            },
                        ),
                    },
                ),
                "d": CmdTree(
                    cmd=None,
                    expect=Expect.Number.value | Expect.Empty.value,
                    children={
                        # "w": CmdTree(
                        #     cmd=DeleteWordCommand(self._text_controller),
                        #     expect=Expect.Any.value,
                        #     children=None
                        # ),
                        "d": CmdTree(
                            cmd=DeleteLineCommand(self._text_controller),
                            expect=Expect.Any.value,
                            children=None,
                        ),
                    },
                ),
                "l": CmdTree(
                    cmd=MoveCursorCommand(self._text_controller, 1),
                    expect=Expect.Empty.value,
                    children=None,
                ),
                "h": CmdTree(
                    cmd=MoveCursorCommand(self._text_controller, -1),
                    expect=Expect.Empty.value,
                    children=None,
                ),
                "o": CmdTree(
                    cmd=NewLineCommand(self._text_controller, wrap=False, above=False),
                    expect=Expect.Empty.value,
                    children=None,
                ),
                "O": CmdTree(
                    cmd=NewLineCommand(self._text_controller, wrap=False, above=True),
                    expect=Expect.Empty.value,
                    children=None,
                ),
            },
        )

    def build_command(
        self, prev_cmd: CmdTree | None, cmd_buf: str, key: Key | str
    ) -> tuple[CmdTree | Command | None, bool]:
        if not key:
            return None, True
        if not prev_cmd:
            prev_cmd = self._commands

        new_cmd = prev_cmd.get(key)
        if new_cmd is None and not Expect.validate(prev_cmd.expect, cmd_buf):
            raise InvalidCommandException
        if isinstance(new_cmd, Command) and cmd_buf:
            new_cmd.set_arg(prev_cmd)
        if isinstance(new_cmd, CmdTree) and new_cmd.cmd is None:
            return new_cmd, False

        return new_cmd, True

    def build_insert_command(self, key: str):
        return InsertCommand(self._text_controller, key)

    def build_new_line_command(self, wrap: bool, above: bool = False):
        return NewLineCommand(self._text_controller, wrap, above)
