from main import send_last_order
from bot import bot
from threading import Thread

bot_front = Thread(target=bot.polling, args=(True, 0))
bot_front.start()
bot_back = Thread(target=send_last_order)
bot_back.start()