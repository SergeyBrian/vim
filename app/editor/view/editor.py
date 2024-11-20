from app.editor.view.base import BaseView
from app.editor.view.command import CommandView
from app.editor.view.text import TextView
from app.ui.render import BaseRenderer


class EditorView(BaseView):
    def __init__(self, renderer: BaseRenderer,
                 text_view: TextView,
                 command_view: CommandView):
        super().__init__(renderer)
        self._text_view = text_view
        self._command_view = command_view

    def init(self):
        self._renderer.init()

    def shutdown(self):
        self._renderer.shutdown()

    def render(self):
        self._text_view.render()
        self._command_view.render()
        self._renderer.render()
