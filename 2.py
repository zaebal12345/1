from binance.client import Client

import json
import requests
from tabletext import to_text

SHOW_ZEROS = False


api_key = 'Oy2a4bZp9hWv8BCYyqmxQZVuXkzwQxSrELCGps63AMM6LzFzJEMmJc6BmUaEhpj6'
secret_key = 'kwdzyjzN6KDjShrxdpA61f3zQt6TauMyaUdYYsV20H8dU9YdvsgG9TSXpurkYHeU'

client = Client(api_key, secret_key)


prices = {item['symbol']: item['price'] for item in client.get_all_tickers()}

BTC_TO_RUB = float(prices.get('BTCRUB'))
BTC_TO_USD = float(prices.get('BTCTUSD'))

def get_price_in_other(balance, coin):
    rub =  float(balance) * float(prices.get('{}RUB'.format(coin), 0))
    usd =  float(balance) * float(prices.get('{}TUSD'.format(coin), 0))
    btc =  float(balance) * float(prices.get('{}BTC'.format(coin), 0))

    if btc == 0:
        btc = rub / BTC_TO_RUB if rub else usd / BTC_TO_USD

    if rub == 0:
        if btc != 0:
            rub = btc * BTC_TO_RUB

    if usd == 0:
        if btc != 0:
            usd = btc * BTC_TO_USD

    if btc == 0:
        btc = rub / BTC_TO_RUB if rub else usd / BTC_TO_USD

    return rub, usd, btc

if __name__ == '__main__':
    result = [
        ['COIN_NAME', 'COIN_BALANCE', 'IN_RUB', 'IN_USD', 'IN_BTC']
    ]

    balances = client.get_account().get('balances')

    total_rub = 0
    total_usd = 0
    total_btc = 0

    for item in balances:
        # balance = client.get_asset_balance(asset=coin)
        # >>> {'asset': 'BTC', 'free': '0.00000000', 'locked': '0.00000000'}

        coin = item.get('asset')
        b = float(item.get('free')) + float(item.get('locked'))

        if float(b) > 0:
            rub, usd, btc = get_price_in_other(b, coin)

            result.append([coin, b, rub, usd, btc])

            total_rub += rub
            total_usd += usd
            total_btc += btc
        else:
            if SHOW_ZEROS:
                result.append([coin, b, 0, 0, 0])

    print(to_text(result))

    print('Всего в rub', total_rub)
    print('Всего в usd', total_usd)
    print('Всего в btc', total_btc)