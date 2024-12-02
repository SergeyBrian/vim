from app.editor.command.editor import EditorCommand


class QuitCommand(EditorCommand):
    def set_arg(self, val):
        pass

    def execute(self):
        self._editor_controller.quit()
