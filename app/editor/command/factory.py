from app.editor.command.command import Command, InvalidCommandException
from app.editor.command.quit import QuitCommand
from app.editor.controllers.editor_interface import EditorControllerInterface
from app.editor.controllers.text import TextController


class CommandFactory:
    def __init__(self,
                 editor_controller: EditorControllerInterface,
                 text_controller: TextController):
        self._editor_controller = editor_controller
        self._text_controller = text_controller

        self._commands = {
            ":q": QuitCommand(editor_controller)
        }

    def build_command(self, cmd: str) -> Command | None:
        if not cmd:
            return None

        if cmd[0] == ":":
            if cmd[-1] != "\n":
                return None
            else:
                cmd = cmd[:-1]

        if cmd not in self._commands:
            raise InvalidCommandException

        return self._commands[cmd]
