from .models import WalletAddress

from luken.utils.txhash import create_tracker


class WalletAddressBackendBase(object):
    coin_type = None

    def get_pubkey(self):
        pass

    def create_wallet(self):
        pass

    def get_address(self, tracking_id):
        wallet_address = WalletAddress.objects.generate(self.coin_type, tracking_id)
        # TODO: generate this URL
        # http://your.api.com/v1/transaction_received?sender=$sender&address=$address&amount=$amount&txhash=$txhash
        callback_url = ""
        create_tracker(
            wallet_address.child, wallet_address.type,
            wallet_address.address, callback_url
        )


class BitcoinAddressBackend(WalletAddressBackendBase):
    coin_type = "BTC"


class EthereumAddressBackend(WalletAddressBackendBase):
    coin_type = "ETH"


class LiteCoinAddressBackend(WalletAddressBackendBase):
    coin_type = "LTC"
