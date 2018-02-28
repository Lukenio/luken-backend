

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
    Bitcoin bakend
    """
    pass


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

    if coin_type == 'bitcoin':
        return BitcoinBackend

    if coin_type == 'litecoin':
        return LitecoinBackend

    if coin_type == 'bitcoincache':
        return BitCoinCash
