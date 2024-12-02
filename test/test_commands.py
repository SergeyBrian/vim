from app.editor.controllers.editor import EditorController
from test_renderer import TestRenderer


def test_quit():
    renderer = TestRenderer(":q\n")
    editor = EditorController(renderer)
    editor.run()


def test_insert():
    renderer = TestRenderer("itestestest")
    editor = EditorController(renderer)
    editor.run()
    assert editor._text_controller._model.get_lines()[0].c_str() == "testestest"


def test_dd():
    renderer = TestRenderer("dd")
    editor = EditorController(renderer)
    editor._text_controller.insert("hello")
    editor.run()
    assert editor._text_controller._model.get_lines()[0].empty()


def test_cursor():
    renderer = TestRenderer("lll")
    editor = EditorController(renderer)
    editor._text_controller.insert("hello")
    editor._text_controller._model._cursor.col = 0
    editor.run()
    assert editor._text_controller._model._cursor.col == 3
