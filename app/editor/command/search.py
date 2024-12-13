from app.editor.command.command import Command


class SearchCommand(Command):
    def __init__(self, controller, model, reversed):
        super().__init__(controller, model)
        self._query = ""
        self._reversed = reversed

    def set_arg(self, val):
        self._query = val.strip()

    def execute(self):
        self._model.search(self._reversed, self._query)


class RepeatSearchCommand(Command):
    def __init__(self, controller, model, reversed):
        super().__init__(controller, model)
        self._reversed = reversed

    def execute(self):
        self._model.repeat_search(self._reversed)
