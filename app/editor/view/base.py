from abc import ABC, abstractmethod

from app.ui.render import BaseRenderer


class BaseView(ABC):
    def __init__(self, renderer: BaseRenderer):
        self._renderer = renderer

    @abstractmethod
    def render(self):
        raise NotImplementedError
