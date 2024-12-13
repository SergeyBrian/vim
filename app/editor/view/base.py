from abc import ABC, abstractmethod

from app.ui.render import IAdapterRenderer


class BaseView(ABC):
    def __init__(self, renderer: IAdapterRenderer):
        self._renderer = renderer

    @abstractmethod
    def render(self):
        raise NotImplementedError
