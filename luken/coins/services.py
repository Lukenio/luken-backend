from importlib import import_module

from django.conf import settings
from django.urls import reverse

from blockchain.v2 import receive

from luken.utils.url import update_url_query_params

BITCOIN_TYPE = "Bitcoin"
ETHEREUM_TYPE = "Ethereum"


class CoinBackendBase:
    """
    This is a base class (interface) to be subclasses if we want to implement
    support for any coin.
    """

    def get_pubkey(self):
        return

    def create_wallet(self, user_id):
        return

    def get_address(self, name):
        return '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2'


class BitcoinBackend(CoinBackendBase):
    """
    Bitcoin backend
    """
    def generate_callback_url(self, tracking_id):
        url = reverse('coin-accounts-process-transaction', args=[tracking_id])
        url = settings.HOST_URL + url
        return update_url_query_params(url, secret=settings.BLOCKCHAIN_CALLBACK_SECRET)

    def get_address(self, tracking_id):
        callback_url = self.generate_callback_url(tracking_id)
        r = receive.receive(settings.BLOCKCHAIN_XPUB, callback_url, settings.BLOCKCHAIN_API_KEY)
        return r.address


class EthereumBackend(CoinBackendBase):
    """
    Ethereum backend
    """
    def get_address(self, name):
        return '0x98dD3568472ecB152C8a42070Ed078AcE577BaB3'


class LitecoinBackend(CoinBackendBase):
    pass


class BitCoinCash(CoinBackendBase):
    pass


def get_coin_backend(coin_type):

    """
    A factory to return backend subclass base on coin_type
    :param coin_type:
    :return:
    """
    # backends = {
    #     BITCOIN_TYPE: BitcoinBackend,
    #     ETHEREUM_TYPE: EthereumBackend,
    #     "litecoin": LitecoinBackend,
    #     "bitcoincache": BitCoinCash,
    # }

    backend_class = settings.COIN_BACKENDS[coin_type]
    module, class_name = backend_class.rsplit(".", maxsplit=1)
    backend_module = import_module(module)
    backend_class = getattr(backend_module, class_name)

    return backend_class()
