from app.editor.utils.keys import Key
from app.ui.render import BaseRenderer, Drawable


class TestRenderer(BaseRenderer):
    def _clear(self, obj: Drawable):
        pass

    def __init__(self, test_input: str):
        super().__init__()
        self._text = test_input
        self._idx = 0

    def init(self):
        pass

    def shutdown(self):
        pass

    def render(self):
        pass

    def getch(self) -> Key | str:
        try:
            res = self._text[self._idx]
            self._idx += 1
            return res
        except IndexError:
            raise KeyboardInterrupt
