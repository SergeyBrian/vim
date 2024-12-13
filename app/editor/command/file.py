from app.editor.command.command import Command
from app.editor.command.quit import QuitCommand
# from app.editor.view import debug as dbg_view


class OpenFileCommand(Command):
    def __init__(self, controller, model):
        super().__init__(controller, model)
        self._filename = ""

    def set_arg(self, val):
        self._filename = val.strip()

    def execute(self):
        try:
            self._controller.open_file(self._filename)
        except Exception as e:
            pass
            # dbg_view.instance().set("file_err", e)


class SaveFileCommand(Command):
    def __init__(self, controller, model):
        super().__init__(controller, model)
        self._filename = ""

    def set_arg(self, val):
        self._filename = val.strip()

    def execute(self):
        try:
            self._controller.save_file(self._filename)
        except Exception as e:
            pass
            # dbg_view.instance().set("file_err", e)


class WriteQuitCommand(SaveFileCommand, QuitCommand):
    def execute(self):
        SaveFileCommand.execute(self)
        QuitCommand.execute(self)
