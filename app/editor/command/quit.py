from app.editor.command.editor import EditorCommand


class QuitCommand(EditorCommand):
    def execute(self):
        self._editor_controller.quit()
