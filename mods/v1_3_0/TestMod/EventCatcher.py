from versions.v1_3_0.fake_main import Game


class EventCatcher:
    def __init__(self):
        super().__init__()

    def OnUpdate(self, parent: Game):
        print("Update Tick!")
