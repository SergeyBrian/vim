import sys

from app.editor.controller.controller import Controller
from app.ui.curses import CursesRenderer


def main():
    renderer = CursesRenderer()
    editor = Controller(renderer)
    filename = sys.argv[1] if len(sys.argv) > 1 else ""
    editor.run(init_file=filename)


if __name__ == "__main__":
    main()
