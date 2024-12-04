from typing import Protocol


class ControllerInterface(Protocol):
    def quit(self): ...
