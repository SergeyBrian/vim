from abc import ABC

from app.editor.command.command import Command
from app.editor.controllers.editor_interface import EditorControllerInterface


class EditorCommand(Command, ABC):
    def __init__(self, editor_controller: EditorControllerInterface):
        self._editor_controller = editor_controller
