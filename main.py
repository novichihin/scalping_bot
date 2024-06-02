import threading
import time
import telebot

import connect_with_user
from handlers import setup_handlers
import requests

import scalping_infrasct
import sqlite3

# Connecting to SQLite
import users_actions

conn = sqlite3.connect('example.db')
cursor = conn.cursor()


# Creating a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (name_user, coin, email)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS coins
                  (coin, price)''')




token = "7030395083:AAGrUzogRvgFPhK-udJ3jgRAbtdV067-OEk"



def run_bot():
    bot = telebot.TeleBot(token)
    setup_handlers(bot)
    bot.polling()


t = threading.Thread(target=run_bot)
t.start()




while True:
    data = scalping_infrasct.get_info_about_coin_cycle("")
    scalping_infrasct.insert_info_to_db(data, cursor, conn)
    print(data)

    time.sleep(2)




