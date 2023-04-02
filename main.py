# поиск в определённой зоне
import os
from time import sleep

import requests as requests
from bs4 import BeautifulSoup
import sqlite3
import telebot
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


bot = telebot.TeleBot(os.environ.get('BOT_KEY'))


def send_last_order():


    con = sqlite3.connect('users.db')
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users").fetchmany()
    while True:
        for user in users:
            html_text = requests.get(user[1]).text
            soup = BeautifulSoup(html_text, 'lxml')
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
