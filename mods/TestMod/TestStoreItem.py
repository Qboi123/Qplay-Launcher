from versions.v1_5_0_pre5.base import StoreItem
from versions.v1_5_0_pre5.fake_main import Game


class TestStoreItem(StoreItem):
    def __init__(self, parent):
        super().__init__(parent)

    def on_buy(self, parent):
        print("TestStoreItem clicked!")
