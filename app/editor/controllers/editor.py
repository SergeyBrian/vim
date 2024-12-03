from app.editor.controllers.command import CommandController
from app.editor.controllers.text import TextController
from app.editor.models.command import CommandModel
from app.editor.models.text import TextModel
from app.editor.view.command import CommandView
from app.editor.view.text import TextView
from app.ui.render import BaseRenderer


class EditorController:
    def __init__(self, renderer: BaseRenderer):
        text_model = TextModel()
        text_view = TextView(renderer, text_model)
        text_controller = TextController(text_model, text_view)
        command_model = CommandModel()
        command_view = CommandView(renderer, command_model)
        self._text_view = text_view
        self._text_controller = text_controller
        self._command_controller = CommandController(
            command_model, command_view, text_controller
        )
        self._command_controller.set_editor_controller(self)
        self._running = True
        self._renderer = renderer

    def run(self):
        try:
            self._renderer.init()
            ch = ""
            while True:
                self._command_controller.handle_key(ch)
                self._text_view.render()
                self._renderer.render()
                if not self._running:
                    break
                ch = self._renderer.getch()
        except KeyboardInterrupt:
            pass
        finally:
            self._renderer.shutdown()

    def quit(self):
        self._running = False
