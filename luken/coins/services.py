from urllib import parse

from django.conf import settings
from django.urls import reverse_lazy

from blockchain.v2 import receive

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
    def get_address(self, tracking_id):
        url = reverse_lazy('coin-accounts-process-transaction', args=[tracking_id])
        url_parts = list(parse.urlparse(url))

        query = dict(parse.parse_qsl(url_parts[4]))
        query.update({"secret": settings.BLOCKCHAIN_CALLBACK_SECRET})

        url_parts[4] = parse.urlencode(query)
        callback_url = parse.urlunparse(url_parts)

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
    backends = {
        BITCOIN_TYPE: BitcoinBackend,
        ETHEREUM_TYPE: EthereumBackend,
        "litecoin": LitecoinBackend,
        "bitcoincache": BitCoinCash,
    }

    backend_class = backends[coin_type]
    return backend_class()
