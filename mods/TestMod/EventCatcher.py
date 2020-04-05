from versions.v1_5_0_pre5.fake_main import Game
# noinspection PyPep8Naming
from versions.v1_5_0_pre5.base import Event
from . import Barier


# noinspection PyUnusedLocal
class EventCatcher(Event):
    def __init__(self):
        super().__init__()

    def on_update(self, parent):
        pass
