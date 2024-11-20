from typing import Protocol


class EditorControllerInterface(Protocol):
    def quit(self): ...
