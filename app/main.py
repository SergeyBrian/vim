from app.editor.controllers.editor import EditorController
from app.ui.curses import CursesRenderer


def main():
    renderer = CursesRenderer()
    editor = EditorController(renderer)
    editor.run()


if __name__ == "__main__":
    main()
