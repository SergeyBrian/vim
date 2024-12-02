from typing import Protocol


class CommandControllerInterface(Protocol):
    def set_state(self, state): ...
