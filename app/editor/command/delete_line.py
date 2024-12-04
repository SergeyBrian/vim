from app.editor.command.command import Command


class DeleteLineCommand(Command):
    def execute(self):
        self._model.delete_line()
