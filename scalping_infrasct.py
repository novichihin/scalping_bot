import requests
from PIL import Image
from io import BytesIO
from matplotlib import pyplot as plt
import folium as f
import numpy as np



def get_info_about_coin_cycle(coin):
    url = f"https://api.freecryptoapi.com/v1/getData?symbol=BTC+ETH"
    headers = {'Authorization': 'Bearer h77qb2uqo6a9956l6ssj'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error: API request failed with status code", response.status_code)


def plot(prices, dates):
    a = np.array(prices)
    b = np.array(dates)
    plt.plot(b, a)

    plt.xlabel("Даты")
    plt.ylabel("Температура")
    plt.legend()
    plt.show()

def get_info_about_coin_to_user(coin, cursor, conn):
    cursor.execute(f'SELECT price FROM coins WHERE coin = ?', (coin,))
    rows = cursor.fetchall()
    prices = [float(row[0]) for row in rows]
    dates = [i + 1.0 for i in range(len(rows))]
    plot(prices, dates)
    return rows


def insert_info_to_db(data, cursor, conn):
    coins = list()
    for coin in data['symbols']:
        coins.append((coin['symbol'], coin['last']))

    
    cursor.executemany('''INSERT INTO coins VALUES (?, ?)''', coins)

    conn.commit()