class EditorModel:
    def __init__(self):
        self._running = True

    def running(self):
        return self._running

    def set_running(self, running: bool):
        self._running = running
