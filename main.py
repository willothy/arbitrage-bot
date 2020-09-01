from catalyst.utils.run_algo import run_algorithm
from catalyst.api import symbol, order
import pandas as pd

def initialize(context):
    context.bittrex = context.exchanges['bitfinex']
    context.poloniex = context.exchanges['poloniex']

    context.bittrex_trading_pair = symbol('eth_btc', context.bittrex.name)
    context.poloniex_trading_pair = symbol('eth_btc', context.poloniex.name)

def handle_data(context, data):
    poloniex_price = data.current(context.poloniex_trading_pair, 'price')
    bittrex_price = data.current(context.bittrex_trading_pair, 'price')

    if poloniex_price > bittrex_price:
        print("Buy on bittrex, sell on poloniex")
        order(
            asset=context.bittrex_trading_pair,
            amount=1,
            limit_price=bittrex_price
        )
        order(
            asset=context.poloniex_trading_pair,
            amount=-1,
            limit_price=poloniex_price
        )
    elif poloniex_price > bittrex_price:
        print("Sell on bittrex, buy on poloniex")
        order(
            asset=context.bittrex_trading_pair,
            amount=-1,
            limit_price=bittrex_price
        )
        order(
            asset=context.poloniex_trading_pair,
            amount=1,
            limit_price=poloniex_price
        )

def analyze():
    pass

run_algorithm(
    initialize=initialize,
    handle_data=handle_data,
    analyze=analyze,
    capital_base=100,
    live=False,
    base_currency='btc',
    exchange_name='bitfinex, poloniex',
    data_frequency='minute',
    start=pd.to_datetime('2020-8-30', utc=True),
    end=pd.to_datetime('2020-8-31', utc=True)
)