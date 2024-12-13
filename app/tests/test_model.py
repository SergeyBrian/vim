import pytest
from mystring import MyString
from app.editor.utils.keys import Key
from app.editor.model.model import Model, Mode


@pytest.fixture
def model():
    return Model()


def test_initial_state(model):
    assert len(model.get_lines()) == 1
    assert model.get_lines()[0].c_str() == ""
    assert model.get_cursor().get() == (0, 0)
    assert model.get_mode() == Mode.NORMAL


def test_load_file(model):
    lines = ["line1", "line2", "line3"]
    model.load_file("test.txt", lines)
    assert len(model.get_lines()) == 3
    assert model.get_lines()[0].c_str() == "line1"
    assert model.get_lines()[1].c_str() == "line2"
    assert model.get_lines()[2].c_str() == "line3"
    assert model.get_cursor().get() == (0, 0)


def test_move_cursor_h(model):
    model.load_file("test.txt", ["abc", "def"])
    model.move_cursor_h(1)
    assert model.get_cursor().get() == (1, 0)
    model.move_cursor_h(1)
    assert model.get_cursor().get() == (2, 0)
    model.move_cursor_h(1)
    # Cursor should not move beyond the end
    assert model.get_cursor().get() == (2, 0)


def test_move_cursor_v(model):
    model.load_file("test.txt", ["abc", "def", "ghi"])
    model.move_cursor_v(1)
    assert model.get_cursor().get() == (0, 1)
    model.move_cursor_v(1)
    assert model.get_cursor().get() == (0, 2)
    model.move_cursor_v(1)
    # Cursor should not move beyond the last line
    assert model.get_cursor().get() == (0, 2)


def test_insert_in_INSERT_mode(model):
    model.set_mode(Mode.INSERT)
    model.insert('h')
    model.insert('i')
    assert model.get_lines()[0].c_str() == "hi"
    assert model.get_cursor().get() == (2, 0)


def test_delete(model):
    model.load_file("test.txt", ["hello", "world"])
    for _ in range(4):
        model.move_cursor_h(1)
    assert model.get_cursor().get() == (4, 0)
    model.delete(1)  # Delete one character
    assert model.get_lines()[0].c_str() == "hell"


def test_delete_line(model):
    model.load_file("test.txt", ["hello", "world", "test"])
    model.move_cursor_v(1)  # Move to "world"
    model.delete_line()
    lines = model.get_lines()
    assert [l.c_str() for l in lines] == ["hello", "test"]
    # Cursor should remain on the same vertical position if possible
    assert model.get_cursor().get() == (0, 0)


def test_copy_paste_line(model):
    model.load_file("test.txt", ["hello", "world"])
    model.move_cursor_v(1)  # Move to 'world'
    model.copy_line(True)
    model.paste()
    lines = model.get_lines()
    assert [l.c_str() for l in lines] == ["hello", "world", "world"]


def test_search(model):
    model.load_file("test.txt", ["abc hello", "world hello", "nope"])
    model.search(False, "hello")
    assert model.get_cursor().get() == (4, 0)


def test_repeat_search(model):
    model.load_file("test.txt", ["abc hello", "world hello", "nope"])
    model.search(False, "hello")
    model.repeat_search(False)
    assert model.get_cursor().get() == (6, 1)


def test_mode_switch(model):
    model.set_mode(Mode.INSERT)
    assert model.get_mode() == Mode.INSERT
    model.set_mode(Mode.NORMAL)
    assert model.get_mode() == Mode.NORMAL


def test_input_buffer(model):
    model.set_input_buffer("command")
    assert model.get_input_buffer() == "command"
    model.push_input_buffer('s')
    assert model.get_input_buffer() == "commands"
    model.push_input_buffer(Key.KEY_LEFT)
    assert model.get_cursor_pos() == len("commands") - 1
    model.push_input_buffer(Key.KEY_BACKSPACE)
    assert model.get_input_buffer() == "commans"


def test_new_line(model):
    model.load_file("test.txt", ["hello"])
    model.new_line(wrap=False, above=False)
    lines = model.get_lines()
    assert [l.c_str() for l in lines] == ["hello", ""]
    assert model.get_cursor().get() == (0, 1)

    model.new_line(wrap=False, above=True)
    lines = model.get_lines()
    assert [l.c_str() for l in lines] == ["hello", "", ""]
    assert model.get_cursor().get() == (0, 1)

    model.set_cursor(0, 2)
    model.new_line(wrap=True, above=False)
    lines = model.get_lines()
    assert [l.c_str() for l in lines] == ["he", "llo", "", ""]
    assert model.get_cursor().get() == (0, 1)
