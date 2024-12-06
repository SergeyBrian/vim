from app.editor.command.command import Command


class HelpCommand(Command):
    def set_arg(self, val):
        pass

    def execute(self):
        self._controller.help()
