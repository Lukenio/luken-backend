from ..services import CoinBackendBase


class TestBackend(CoinBackendBase):
    def get_address(self, name):
        return "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"
