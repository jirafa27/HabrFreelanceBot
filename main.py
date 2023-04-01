# поиск в определённой зоне
from time import sleep

import requests as requests
from bs4 import BeautifulSoup
import sqlite3

import telebot

bot = telebot.TeleBot('5892722843:AAFtxA1hpDSD4MRgXB0Epf26bxGmv6zJcDE')




def start_bot():
    url = 'https://freelance.habr.com/tasks?categories=development_backend,development_bots,development_scripts'

    html_text = requests.get(url).text

    # используем парсер lxml
    soup = BeautifulSoup(html_text, 'lxml')

    con = sqlite3.connect('users.db')
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users").fetchmany()
    while True:
        for user in users:
            tasks = soup.find('ul', class_='content-list_tasks')
            list_tasks = tasks.find_all('li', class_='content-list__item')
            for task in list_tasks:
                published_at = task.find('span', class_='params__published-at').find('span').text
                if published_at.startswith("~"):
                    break
                if int(published_at[:2])>10:
                    break
                bot.send_message(user[0], f"{task.text} \n https://freelance.habr.com/{task.find_all('a')[0]['href']}")
        sleep(600)
