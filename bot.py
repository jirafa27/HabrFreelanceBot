import sqlite3

import telebot
from telebot import types

from exceptions import NoSuchUserException

bot = telebot.TeleBot('5892722843:AAFtxA1hpDSD4MRgXB0Epf26bxGmv6zJcDE')



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "👋 Привет! Я отправляю новые заказы на хабр-фриланс")

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



@bot.message_handler(commands=['add_url'])
def add_url(message):
    try:
        check_if_user_exists(message.from_user.id)
        url = message.text.split(' ')[1]
        add_url_to_db(url, message.from_user.id)
    except NoSuchUserException:
        bot.send_message(message.from_user.id, "Вы не подписаны")
    except IndexError:
        bot.reply_to(message, "Введите url")
        bot.register_next_step_handler(message, get_and_add_url)

def get_and_add_url(message):
    url = message.text
    try:
        add_url_to_db(url, message.from_user.id)
        bot.send_message(message.from_user.id, "Если Вы правильно ввели урл, то вам будут приходить сообщения о новых заказах по выбранным категориям")
    except NoSuchUserException:
        bot.send_message(message.from_user.id, "Вы не подписаны")

def check_if_user_exists(chat_id):
    con = sqlite3.connect('users.db')
    res = con.execute(f"SELECT * FROM users WHERE chat_id={chat_id}").fetchmany()
    if not res:
        raise NoSuchUserException
    con.close()

def add_url_to_db(url, chat_id):
    con = sqlite3.connect('users.db')
    con.execute(f"UPDATE users SET subscribe_url='{url}' WHERE chat_id={chat_id}")
    con.commit()
    con.close()


