from versions.v1_5_0_pre2.fake_main import Game


# noinspection PyMethodMayBeStatic
class Initialize:
    def __init__(self):
        self.ID = "TestMod"

    def pre_initialize(self, parent: Game):
        from .TestStoreItem import TestStoreItem
        from .EventCatcher import EventCatcher
        self.test_store_item = TestStoreItem(parent)
        self.events = [EventCatcher()]
        print("Pre-Inialized!")
        print("Parent:", parent)
        print("Parent Dictionary:", parent.__dict__)

    def post_initialize(self, parent):
        print("Post-Inialized!")
        print("Parent:", parent)
        print("Parent Dictionary:", parent.__dict__)


