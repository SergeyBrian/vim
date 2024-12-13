from abc import ABC, abstractmethod


class Observable(ABC):
    @abstractmethod
    def register_subscriber(callback_fn):
        raise NotImplementedError
