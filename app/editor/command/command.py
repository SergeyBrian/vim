from abc import ABC, abstractmethod


class InvalidCommandException(Exception):
    pass


class Command(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError
