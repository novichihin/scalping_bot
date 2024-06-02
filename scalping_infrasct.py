import pandas as pd
import requests
import math
from matplotlib import pyplot as plt
import numpy as np


index_img = 0


def get_info_about_coin_cycle(coin):
    url = f"https://api.freecryptoapi.com/v1/getData?symbol=BTC+ETH+XPR+LTC+SOL"
    headers = {"Authorization": "Bearer h77qb2uqo6a9956l6ssj"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error: API request failed with status code", response.status_code)


import matplotlib.pyplot as plt
import numpy as np

index_img = 0


def plot(prices, dates, coin):
    global index_img

    a = np.array(prices)
    b = np.array(dates)

    plt.figure(figsize=(10, 6))  # Увеличиваем размер графика

    plt.plot(
        b, a, marker="o", linestyle="-", color="#007bff", linewidth=1.5
    )  # Изменяем стиль линий и маркеры

    plt.xlabel("Дата", fontsize=12, color="#666")
    plt.ylabel("Цена", fontsize=12, color="#666")
    plt.title(f"График цены {coin}", fontsize=18, color="#333")  # Добавляем заголовок

    plt.xticks(
        rotation=45, fontsize=10, color="#999"
    )  # Поворачиваем метки оси X для лучшей читаемости
    plt.yticks(fontsize=10, color="#999")

    plt.grid(
        True, color="#ddd", linestyle="--", linewidth=0.5
    )  # Добавляем сетку для лучшей ориентации

    plt.tight_layout()  # Улучшаем расположение элементов графика

    plt.savefig(f"png_temp/plot{index_img}.png", transparent=True, dpi=100)

    index_img += 1

    return f"png_temp/plot{index_img - 1}.png"


def get_limit(period):
    limit = 0
    if period == "1min":
        limit = 60 / 2
    if period == "5min":
        limit = 300 / 2
    if period == "10min":
        limit = 600 / 2
    if period == "30min":
        limit = 1800 / 2

    print(limit)
    return limit


def get_graph_about_coin_to_user(
    coin, cursor, conn, period
):  # при нажатии на кнопку коина пользователем выполняется это
    limit = get_limit(period)
    cursor.execute(f"SELECT price FROM coins WHERE coin = ? LIMIT?", (coin, limit))
    rows = cursor.fetchall()
    prices = [float(row[0]) for row in rows]
    dates = [i + 1.0 for i in range(len(rows))]
    str = plot(prices, dates, coin)  # вывод картинки графика
    return str


def get_analitics_about_coin_to_user(coin, cursor, conn, period):
    limit = get_limit(period)
    cursor.execute(f"SELECT price FROM coins WHERE coin = ? LIMIT?", (coin, limit))
    rows = cursor.fetchall()
    df = [float(row[0]) for row in rows]
    avg = sum(df) / len(df)
    maxx = max(df)
    minn = min(df)
    res = list()
    res.append(avg)
    res.append(maxx)
    res.append(minn)
    return res


def insert_info_to_db(data, cursor, conn):  # заносим в бд coin-price
    coins = list()
    for coin in data["symbols"]:
        coins.append((coin["symbol"], coin["last"]))

    cursor.executemany("""INSERT INTO coins VALUES (?, ?)""", coins)

    conn.commit()
