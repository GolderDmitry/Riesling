import time, datetime, PostgresAPI
from decimal import Decimal

import GYobitAPI


class Constructor:

    yobit = None
    db = None

    def __init__(self):
        self.yobit = GYobitAPI.GYobitAPI()
        self.db = PostgresAPI.PostgresAPI()
        self.db.__createPermissionTable__()
        self.db.__addBotInPermissionTable__()

    # Добавить пользователя
    def addUser(self, message, bot_key):
        user = self.db.getPermissionById(message.chat.id, bot_key)

        # Если пользователя нет, то добавляем его
        if user is None or user.__len__() == 0:
            created = int(time.time())
            changed = int(time.time())
            self.db.setPermission(message.chat.first_name, message.chat.last_name, message.chat.id, created, changed, bot_key)

        return self.db.getPermissionById(message.chat.id, bot_key)[0]

    def getUsers(self, bot_key):
        users = list(self.db.getPermissions(bot_key))
        users_id = []
        for user in users:
            users_id.append(user[4])
        return users_id

    def deleteUser(self, message, bot_key):
        self.db.deletePermissionById(message.chat.id, bot_key)

    # Получить баланс аккаунта
    def getBalanse(self):
        balance = ""
        user_info = self.yobit.get_user_info()
        try:
            coins = user_info['return']['funds']
            for key in coins:
                if Decimal(coins[key]) > 0.00001:
                    balance += f"{key}:  {round(Decimal(coins[key]), 8)}\n"
        except:
            print("Error balance")
        return balance

    # Получить баланс монеты
    def getBalanseByCoin(self, coin):
        balance = 0
        user_info = self.yobit.get_user_info()
        try:
            balance = user_info['return']['funds'][coin]
        except:
            print("Error balance")
        return balance

    # Получить текущие ордера
    def getOrders(self, pairs):
        result = ""
        orders = self.yobit.active_orders(pairs)

        if orders is not None:
            for key in orders:
                if key == 'return':
                    order_id = list(orders[key].keys())[0]
                    result += f"ID: {order_id}\n"
                    result += f"PAIR: {orders[key][order_id]['pair']}\n"
                    result += f"TYPE: {orders[key][order_id]['type']}\n"
                    result += f"AMOUNT: {orders[key][order_id]['amount']}\n"
                    result += f"PRICE: {round(orders[key][order_id]['rate'], 8)}\n"
                    result += f"STATUS: {orders[key][order_id]['status']}\n"
                    result += f"DATE: {datetime.datetime.fromtimestamp(int(orders[key][order_id]['timestamp_created']))}\n"
                    result += f"-----------------------"

        return result


    # Выставить ордер
    def setOrder(self, pair, trade_type, rate, amount):
        result = None
        try:
            result = self.yobit.trade(pair, trade_type, rate, amount)
        except:
            print(f"Error {trade_type} {pair} {rate} {amount}")
        return result

    # Удалить ордер
    def deleteOrder(self, order_id):
        balance = ""
        try:
            result = self.yobit.cancel_order(order_id)
            if result['success'] == 1:
                coins = result['return']['funds']
                for key in coins:
                    if Decimal(coins[key]) != "":
                        balance += f"{key}:  {round(Decimal(coins[key]), 8)}\n"
            else:
                balance = "Incorrect order_id"
        except:
            balance = "Error return balance"

        return balance