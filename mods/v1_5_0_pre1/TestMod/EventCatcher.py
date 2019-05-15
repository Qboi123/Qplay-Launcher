from versions.v1_5_0_pre1.fake_main import Game
# noinspection PyPep8Naming
from versions.v1_5_0_pre1.base import Event
from . import Barier


# noinspection PyUnusedLocal
class EventCatcher(Event):
    def __init__(self, parent: Game):
        super().__init__(parent)
        self.parent = parent

    def on_update(self, parent: Game):
        Barier
