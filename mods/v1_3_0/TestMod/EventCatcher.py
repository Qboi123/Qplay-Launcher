from versions.v1_3_0.fake_main import Game


# noinspection PyUnusedLocal
class EventCatcher:
    def __init__(self, parenr: Game):
        super().__init__()
        self.parenr = parenr

    def OnUpdate(self, parent: Game):
        print("Update Tick!")
