import time

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



while True:
    data = scalping_infrasct.get_info_about_coin_cycle("")
    scalping_infrasct.insert_info_to_db(data, cursor, conn)
    print(data)

    time.sleep(10)
