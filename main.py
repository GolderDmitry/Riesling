import datetime

import telebot, PgAPI, logging
from telebot import types
from settings import API_TOKEN

logging.basicConfig(
        filename="Riesling.log",
        filemode="w",
        format="%(asctime)s: [%(levelname)s] PID: %(process)d: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
bot = telebot.TeleBot(API_TOKEN)
db = PgAPI.PgAPI()
permission = None

@bot.message_handler(commands=['start'])
def start(message):
    #Получаем переменные учетной записи
    last_name = bot.get_chat(message.chat.id).last_name
    first_name = bot.get_chat(message.chat.id).first_name
    memberInfo = {
        "last_name": last_name,
        "first_name": first_name,
        "user_id": message.chat.id
    }

    db._insertPermissionMember(memberInfo)

    if db.getMemberPermission(message.chat.id) == 1000:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Ордера")
        btn2 = types.KeyboardButton("Логи")
        btn3 = types.KeyboardButton("Пользователи")
        btn4 = types.KeyboardButton("Пары")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text="МЕНЮ: ".format(message.from_user), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text=f"Пользователь {last_name} {first_name} добавлен")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if (message.text == "Ордера"):
        if db.getMemberPermission(message.chat.id) == 1000:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("CREATED")
            btn2 = types.KeyboardButton("FINISHED")
            back = types.KeyboardButton("назад")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text="ВЫБЕРИТЕ ТИП ОРДЕРА", reply_markup=markup)

    elif (message.text == "Пары"):
        if db.getMemberPermission(message.chat.id) == 1000:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("eth_rur")
            back = types.KeyboardButton("назад")
            markup.add(btn1, back)
            bot.send_message(message.chat.id, text="ВЫБЕРИТЕ ПАРУ", reply_markup=markup)

    elif (message.text == "CREATED"):
        if db.getMemberPermission(message.chat.id) == 1000:
            inform = db.getCreatedOrders()
            bot.send_message(message.chat.id, text=inform)

    elif (message.text == "FINISHED"):
        if db.getMemberPermission(message.chat.id) == 1000:
            inform = db.getFinishedOrders()
            bot.send_message(message.chat.id, text=inform)

    elif (message.text == "назад"):
        if db.getMemberPermission(message.chat.id) == 1000:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Ордера")
            btn2 = types.KeyboardButton("Логи")
            btn3 = types.KeyboardButton("Пользователи")
            btn4 = types.KeyboardButton("Пары")
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, text="МЕНЮ", reply_markup=markup)

    elif (message.text == "Пользователи"):
        if db.getMemberPermission(message.chat.id) == 1000:
            inform = db.getMembersInfo()
            bot.send_message(message.chat.id, text=inform)

    elif (message.text == "Логи"):
        if db.getMemberPermission(message.chat.id) == 1000:
            inform = db.getLogInfo(30)
            bot.send_message(message.chat.id, text=inform)

    elif (message.text == "eth_rur"):
        if db.getMemberPermission(message.chat.id) == 1000:
            pairs = db.getPairsInfo("eth_rur")
            inform = ""
            inform += f"{datetime.datetime.fromtimestamp(pairs[0][15])}\n" \
                      f"SELL: ({pairs[0][11]}) {pairs[0][12]}\n" \
                      f"BUY: ({pairs[0][13]}) {pairs[0][14]}\n" \
                      f"\n" \
                      f"MIN: {pairs[0][2]}\n" \
                      f"MAX: {pairs[0][3]}\n" \
                      f"LAST: {pairs[0][4]}\n" \
                      f"\n" \
                      f"BUY: {pairs[0][5]}\n" \
                      f"SELL: {pairs[0][6]}"
            bot.send_message(message.chat.id, text=inform)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)


