from app.editor.controllers.command import CommandController
from app.editor.controllers.editor import EditorController
from app.editor.controllers.text import TextController
from app.editor.models.command import CommandModel
from app.editor.models.editor import EditorModel
from app.editor.models.text import TextModel
from app.editor.utils.keys import Key
from app.editor.view.command import CommandView
from app.editor.view.editor import EditorView
from app.editor.view.text import TextView
from app.ui.curses import CursesRenderer
from app.ui.render import Text


def main():
    renderer = CursesRenderer()
    text_view = TextView(renderer)
    text_model = TextModel()
    text_controller = TextController(text_model, text_view)
    command_model = CommandModel()
    command_view = CommandView(renderer)
    command_controller = CommandController(command_model, command_view, text_controller)
    editor_model = EditorModel()
    editor_view = EditorView(renderer, text_view, command_view)
    editor = EditorController(editor_model, editor_view, command_controller)

    try:
        editor_view.init()

        ch = ""
        while True:
            editor.process_key(ch)
            text_view._renderer.add(Text(0, 0, f"{ch}"))
            if not editor.running():
                break
            ch = renderer.getch()
    except KeyboardInterrupt:
        pass
    finally:
        editor_view.shutdown()


if __name__ == "__main__":
    main()
