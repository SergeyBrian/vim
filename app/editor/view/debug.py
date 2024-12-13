from typing import Any

from app.ui.render import IAdapterRenderer, Text, Window, Drawable, Alignment


class DebugView:
    def __init__(self, renderer: IAdapterRenderer):
        self._renderer = renderer
        self._dbg_items: dict[str, Any] = {}

    def set(self, name: str, item):
        self._dbg_items[name] = item

    def _render(self):
        return
        self._renderer.add(
            Window(h=1., w=0.5, items=[
                Text(0, 0, "Debug info:"),
                *[
                    Text(0, i + 1, f"{name}: {val.__str__()}")
                    for i, (name, val) in enumerate(self._dbg_items.items())
                ]
            ], alignment=Alignment.Right),
            priority=99
        )


_dbg_view: DebugView


def init(renderer: IAdapterRenderer):
    global _dbg_view
    _dbg_view = DebugView(renderer)
    renderer.add_pre_callback(_dbg_view._render)


def instance() -> DebugView:
    global _dbg_view
    return _dbg_view
