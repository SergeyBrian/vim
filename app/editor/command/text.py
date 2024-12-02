from abc import ABC

from app.editor.command.command import Command
from app.editor.controllers.editor_interface import EditorControllerInterface
from app.editor.controllers.text import TextController


class TextCommand(Command, ABC):
    def __init__(self, text_controller: TextController):
        self._text_controller = text_controller
