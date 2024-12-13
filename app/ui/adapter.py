from app.ui.render import IAdapterRenderer
from app.ui.controller import IAdapterController


class Adapter(IAdapterController, IAdapterRenderer):
    pass
