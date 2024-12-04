from app.editor.controller.controller import Controller
from app.ui.curses import CursesRenderer


def main():
    renderer = CursesRenderer()
    editor = Controller(renderer)
    editor.run()


if __name__ == "__main__":
    main()
