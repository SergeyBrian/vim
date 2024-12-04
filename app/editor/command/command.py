from abc import ABC, abstractmethod

from app.editor.controller.interface import ControllerInterface
from app.editor.model.interface import TextModel


class InvalidCommandException(Exception):
    pass


class Command(ABC):
    def __init__(self, controller: ControllerInterface, model: TextModel):
        self._controller: ControllerInterface = controller
        self._model: TextModel = model

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def set_arg(self, val):
        pass
