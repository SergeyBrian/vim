from abc import ABC, abstractmethod
from enum import Enum

from app.editor.utils.keys import Key


class Alignment(Enum):
    Bottom = 1
    Right = 2
    MiddleHorizontal = 3
    MiddleVertical = 4
    Center = 5


class Drawable(ABC):
    def __init__(self,
                 x: int | float | None,
                 y: int | float | None,
                 w: int | float | None = None,
                 h: int | float | None = None,
                 alignment: Alignment | None = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alignment = alignment
        self._hash = hash((type(self).__name__, self.x, self.y, self.w, self.h, self.alignment))

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return self._hash == other.__hash__()

    def resolve_geometry(self, height: int, width: int):
        if isinstance(self.x, float):
            self.x = int(self.x * width)
        if isinstance(self.y, float):
            self.y = int(self.y * height)
        if isinstance(self.w, float):
            self.w = int(self.w * width)
        if isinstance(self.h, float):
            self.h = int(self.h * height)

        if not self.x:
            self.x = 0
        if not self.y:
            self.y = 0
        if not self.w:
            self.w = 0
        if not self.h:
            self.h = 0

        if not self.alignment:
            return

        if self.alignment == Alignment.Bottom:
            self.y = height - self.h
        elif self.alignment == Alignment.Right:
            self.x = width - self.w
        elif self.alignment == Alignment.MiddleVertical:
            self.y = (height - self.h) // 2
        elif self.alignment == Alignment.MiddleHorizontal:
            self.x = (width - self.w) // 2
        elif self.alignment == Alignment.Center:
            self.y = (height - self.h) // 2
            self.x = (width - self.w) // 2


class Text(Drawable):
    def __init__(self, x: int | float, y: int | float, text: str, alignment: Alignment | None = None):
        super().__init__(x, y, w=len(text), h=1, alignment=alignment)
        self.text = text


class Window(Drawable):
    def __init__(self,
                 h: int | float,
                 w: int | float,
                 items: list[Drawable],
                 x: int | float | None = None,
                 y: int | float | None = None,
                 alignment: Alignment | None = None):
        super().__init__(x, y, w, h, alignment)
        self.items = items
        self.alignment = alignment


class Cursor(Drawable):
    pass


class BaseRenderer(ABC):
    def __init__(self):
        self._draw_calls: list[Drawable] = []

    @abstractmethod
    def init(self):
        raise NotImplementedError

    @abstractmethod
    def shutdown(self):
        raise NotImplementedError

    @abstractmethod
    def render(self):
        raise NotImplementedError

    @abstractmethod
    def getch(self) -> Key | str:
        raise NotImplementedError

    @abstractmethod
    def _clear(self, obj: Drawable):
        raise NotImplementedError

    def add(self, obj: Drawable):
        # if obj in self._draw_calls:
        #     self._clear(obj)
        # else:
        self._draw_calls.append(obj)
