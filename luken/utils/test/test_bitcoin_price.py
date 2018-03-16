from django.test import TestCase

from luken.utils.bitcoin_price import get_bitcoin_price


class BitcoinPriceTestCase(TestCase):

    def test_get_bitcoin_price(self):
        price = get_bitcoin_price()
        self.assertGreater(price, 0)
