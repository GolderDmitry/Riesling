import datetime

import telebot, Constructor
from telebot import types
from settings import BOT_TOKEN, BOT_KEY

bot = telebot.TeleBot(BOT_TOKEN);
constructor = Constructor.Constructor()

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
    f"""/start - подписаться на мониторинг
/stop - отменить подписку на мониторинг
/balance - баланс счета
/orders - выставленные ордера
/del - удалить ордер  (id)
/sell - продать (pair) кол-вл (amount) за (price)
/buy - купить (pair) кол-вл (amount) за (price)
        """)

@bot.message_handler(commands=['start'])
def start_message(message):
    user = constructor.addUser(message, BOT_KEY)
    if user is not None:
        bot.send_message(
            message.chat.id,
            f"""
USER: {user[2]} {user[3]}
ID: {user[0]}
RIGHTS: {user[1]}
DATE:  {datetime.datetime.fromtimestamp(user[6])}
BOT:️ {user[7]}
                """)

@bot.message_handler(commands=['stop'])
def start_message(message):
    constructor.deleteUser(message, BOT_KEY)
    bot.send_message(message.chat.id, "Мониторинг остановлен")

@bot.message_handler(commands=['balance'])
def start_message(message):
    balance = constructor.getBalanse()
    if balance != "":
        bot.send_message(message.chat.id, balance)

@bot.message_handler(commands=['orders'])
def start_message(message):
    orders = constructor.getOrders("btc_rur")
    if orders != "":
        bot.send_message(message.chat.id, orders)
    else:
        bot.send_message(message.chat.id, "Empty")

@bot.message_handler(commands=['del'])
def start_message(message):
    try:
        order_id = message.text.split(' ')[1]
        bot.send_message(message.chat.id, constructor.deleteOrder(order_id))
    except:
        bot.send_message(message.chat.id, "No one parameter")


@bot.message_handler(commands=['sell'])
def start_message(message):
    try:
        datas = message.text.split(' ')
        if datas.__len__() == 2:
            sellCoin = datas[1].split('_')[0]
            bot.send_message(message.chat.id, constructor.getBalanseByCoin(sellCoin))
        if datas.__len__() == 4:
            pair = datas[1]
            amount = datas[2]
            price = datas[3]
            trade = constructor.setOrder(pair, 'sell', price, amount)
            if trade['success'] == 1:
                bot.send_message(message.chat.id, f"NEW ORDER: ID - {trade['return']['order_id']}")
            else:
                a = 1
                bot.send_message(message.chat.id, f"NEW {trade['error']}")
    except:
        bot.send_message(message.chat.id, "Miss params (pair) (amount) (price)")

@bot.message_handler(commands=['buy'])
def start_message(message):
    try:
        datas = message.text.split(' ')
        if datas.__len__() == 2:
            sellCoin = datas[1].split('_')[0]
            bot.send_message(message.chat.id, constructor.getBalanseByCoin(sellCoin))
        if datas.__len__() == 4:
            pair = datas[1]
            amount = datas[2]
            price = datas[3]
            trade = constructor.setOrder(pair, 'buy', price, amount)
            bot.send_message(message.chat.id, constructor.getBalanseByCoin(sellCoin))
    except:
        bot.send_message(message.chat.id, "Miss params (pair) (amount) (price)")

if __name__ == '__main__':
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)


