import sqlite3

import telebot
from telebot import types

bot = telebot.TeleBot('5892722843:AAFtxA1hpDSD4MRgXB0Epf26bxGmv6zJcDE')



@bot.message_handler(commands=['start'])
def start(message):
    subscribe_button = types.KeyboardButton("Подписаться")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(subscribe_button)
    bot.send_message(message.from_user.id, "👋 Привет! Я отправляю новые заказы на хабр-фриланс", reply_markup=markup)

@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    try:
        cur.execute(f"INSERT INTO users (chat_id, subscribe_url)"
                    f"VALUES ({message.from_user.id}, NULL);")
        con.commit()
        con.close()
        bot.send_message(message.from_user.id, "Подписка успешно оформлена")
    except:
        bot.send_message(message.from_user.id, "Вы уже подписаны")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute(f"DELETE FROM users WHERE chat_id={message.from_user.id};")
    con.commit()
    con.close()
    bot.send_message(message.from_user.id, "Вы успешно отписались")