from versions.v1_5_0_pre3.base import StoreItem
from versions.v1_5_0_pre3.fake_main import Game


class TestStoreItem(StoreItem):
    def __init__(self, parent: Game):
        super().__init__(parent)

    def on_buy(self, parent: Game):
        print("TestStoreItem clicked!")
