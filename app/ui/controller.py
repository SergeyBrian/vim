from abc import ABC, abstractmethod
from app.editor.utils.keys import Key


class IAdapterController(ABC):
    @abstractmethod
    def getch(self) -> Key | str:
        raise NotImplementedError
