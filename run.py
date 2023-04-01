from main import start_bot
from bot import bot
from threading import Thread

bot_front = Thread(target=bot.polling, args=(True, 0))
bot_front.start()
bot_back = Thread(target=start_bot)
bot_back.start()