from app.ui.render import BaseRenderer


class UI:
    def __init__(self, renderer: BaseRenderer):
        self._renderer: BaseRenderer = renderer

