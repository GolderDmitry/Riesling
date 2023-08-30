# Original code was found on https://qna.habr.com/q/515393
import hmac
import hashlib
import requests
import time
from urllib.parse import urlencode
from settings import Y_KEY, Y_SECRET
from settings import Y_BASE_URL

PUBLIC_API = f"{Y_BASE_URL}/api/3/"
TRADE_API = f"{Y_BASE_URL}/tapi"


class GYobitAPI:

    key = None
    secret = None
    host = None
    database = None

    def __init__(self):
        self.key = Y_KEY
        self.secret = Y_SECRET


    ######################################################################
    ##### Public API section
    ######################################################################
    def __api_query_public(self, method, pair=None, options=None):

        result = None

        if not options:
            options = {}
        if not pair:
            pair = ''

        request_url = PUBLIC_API + method
        if pair != '':
            request_url += '/' + pair.lower() + '/'
        if options != {}:
            request_url += '?'
            request_url += urlencode(options)

        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "uru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
        }

        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            try:
                result = response.json()
            except ConnectionError as error:
                print(f"{error}")
        else:
            while response.status_code != 200:
                time.sleep(5)
                response = requests.get(request_url, headers=headers)
            try:
                result = response.json()
            except ConnectionError as error:
                print(f"{error}")

        return result

    def info(self):
        ##############################################################################
        #Used to get about server time and coin pares of the YoBit market.
        #Response contains min_price, max_price, min_amount, and fee for each pair.
        #:return: JSON of pairs with info
        #:rtype : dict
        ##############################################################################
        return self.__api_query_public('info')

    def ticker(self, pair):

        ##############################################################################
        #Used to get statistic data for the last 24 hours for selected pair.
        #Response contains hight, low, avg, vol, vol_cur, last, buy, sell fields for the pair.
        #:param pair: Pair of currencies, example 'ltc_btc'
        #:type pair: str
        #:return: Statistic
        #:rtype : dict
        ##############################################################################

        return self.__api_query_public('ticker', pair)

    def depth(self, pair, limit=150):
        ##############################################################################
        #Used to get information about lists of active orders for selected pair.
        #Response contains asks and bids lists for the pair.
        #:param pair: Pair of currencies, example 'ltc_btc'
        #:type pair: str
        #:param limit: Size of response (on default 150 to 2000 max)
        #:type limit: int
        #:return: Current information about active orders
        #:rtype : dict
        ##############################################################################
        return self.__api_query_public('depth', pair, {'limit': limit})

    def trades(self, pair, limit=150):
        ##############################################################################
        #Used to get information about the last transactions of selected pair.
        #Response contains type, price, amount, tid, timestamp for each transaction.
        #:param pair: Pair of currencies, example 'ltc_btc'
        #:type pair: str
        #:param limit: Size of response (on default 150 to 2000 max)
        #:type limit: int
        #:return: Current information about transactions
        #:rtype : dict
        ##############################################################################
        return self.__api_query_public('trades', pair, {'limit': limit})

    ######################################################################
    ##### Trade API section
    ######################################################################
    def __api_query_trade(self, method, params=None):

        result = None
        response = None

        if params is None:
            params = {}

        params['method'] = method
        params['nonce'] = str(int(time.time()))

        signature = hmac.new(self.secret.encode(), urlencode(params).encode(), hashlib.sha512).hexdigest()

        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "uru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
            "Content-Type": "application/x-www-form-urlencoded",
            "Key": self.key,
            "Sign": signature
        }

        response = requests.post(url=TRADE_API, data=params, headers=headers)
        if response.status_code == 200:
            if response.content.__len__() > 18:
                try:
                    result = response.json()
                except ConnectionError as error:
                    print(f"{error}")
            elif response.content.__len__() <= 18:
                result = None
        else:
            while response.status_code != 200:
                time.sleep(5)
                response = requests.post(url=TRADE_API, data=params, headers=headers)

            try:
                if response.text.__len__() > 50:
                    result = response.json()
                    if result['success'] == 0:
                        result = None
                    else:
                        print(f"JSON read success")
            except ConnectionError as error:
                result = None
                print(f"{error}")

        return result

    def get_user_info(self):
        ##############################################################################
        #Used to get information about user's balances and priviledges of API-key
        #as well as server time. Response contains funds, fund_incl_orders, rights,
        #transaction_count, open_orders, server time.
        #:return: JSON with info
        #:rtype : dict
        ##############################################################################
        return self.__api_query_trade('getInfo')

    def trade(self, pair, trade_type, rate, amount):
        ##############################################################################
        #Used to create new orders for stock exchange trading
        #:param pair: Pair of currencies, example 'ltc_btc'
        #:type pair: str
        #:param trade_type: 'buy' or 'sell'
        #:type trade_type: str
        #:param rate: Exchange rate for buying or selling
        #:type rate: float
        #:param amount: Amount of needed for buying or selling
        #:type amount: float
        #:return: Success, info about the order, order_id.
        #:rtype : dict
        ##############################################################################
        return self.__api_query_trade('Trade', {'pair': pair, 'type': trade_type, 'rate': rate, 'amount': amount})

    def active_orders(self, pair):
        ##############################################################################
        #Used to get list of user's active orders.
        #:param pair: Pair of currencies, example 'ltc_btc'
        #:type pair: str
        #:return: List of orders byu order_id
        #:rtype : dict
        ##############################################################################
        return self.__api_query_trade('ActiveOrders', {'pair': pair})

    def order_info(self, order_id):
        ##############################################################################
        #Used to get detailed information about the chosen order.
        #Response contains pair, type, start_amount, amount, rate,
        #timestamp_created, status for the order.
        #:param order_id: Order ID
        #:type order_id: int
        #:return: JSON of the order
        #:rtype : dict
        ##############################################################################
        return self.__api_query_trade('OrderInfo', {'order_id': order_id})

    def cancel_order(self, order_id):
        ##############################################################################
        #Used to cancel the choosen order.
        #:param order_id: Order ID
        #:type order_id: int
        #:return: Success and balances active after request
        #:rtype : dict
        ##############################################################################
        return self.__api_query_trade('CancelOrder', {'order_id': order_id})

    def trade_history(self, pair, from_start=0, count=1000, from_id=0, end_id=100000000000,
                      order='DESC', since=0, end=time.time() + 1000):
        ##############################################################################
        #Used to retrieve transaction history.
        #Response contains list of transactions with pair, type,
        #amount, rate, order_id, is_your_order and timestamp for each transaction.
        #:param pair: Pair of currencies, example 'ltc_btc'
        #:type pair: str
        #:param from_start: Number of transaction from which response starts (default 0)
        #:type from_start: int
        #:param count: Quantity of transactions in response (default 1000)
        #:type count: int
        #:param from_id: ID of transaction from which response start (default 0)
        #:type from_id: int
        #:param end_id: ID of trnsaction at which response finishes (default inf)
        #:type end_id: int
        #:param order: Sorting order, 'ASC' for ascending and 'DESC' for descending
        #:type order: str
        #:param since: The time to start the display (unix time, default 0)
        #:type since: int
        #:param end: The time to end the display (unix time, default inf)
        #:type end: int
        #:return: List of transactions
        #:rtype : dict
        ##############################################################################
        options = {
            'from': from_start,
            'count': count,
            'from_id': from_id,
            'end_id': end_id,
            'order': order,
            'since': since,
            'end': end,
            'pair': pair
        }
        return self.__api_query_trade('TradeHistory', options)

    def get_deposit_address(self, coin_name, need_new=False):
        ##############################################################################
        #Used to get deposit address.
        #:param coin_name: The name of a coin, example 'BTC'
        #:type coin_name: str
        #:param need_new: True or False
        #:type need_new: bool
        #:return: Wallet address
        #:rtype : dict
        ##############################################################################
        options = {'coinName': coin_name, 'need_new': 1 if need_new else 0}
        return self.__api_query_trade('GetDepositAddress', options)

    def withdraw_coins_to_address(self, coin_name, amount, address):
        ##############################################################################
        #Used to create withdrawal request.
        #:param coin_name: The name of a coin, example 'BTC'
        #:type coin_name: str
        #:param amount: Amount to withdraw
        #:type amount: float
        #:param address: Destination address
        #:type address: str
        #:return: Success and server time
        #:rtype : dict
        ##############################################################################
        options = {'coinName': coin_name, 'amount': amount, 'address': address}
        return self.__api_query_trade('WithdrawCoinsAddress', options)
