from decimal import Decimal

from coinmarketcap import Market

market = Market()


def get_bitcoin_price():
    r = market.ticker("bitcoin")[0]
    return Decimal(r["price_usd"])
