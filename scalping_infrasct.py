import requests

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


def plot(prices, dates):
    global index_img

    a = np.array(prices)
    b = np.array(dates)

    plt.figure(figsize=(10, 6))  # Увеличиваем размер графика

    plt.plot(
        b, a, marker="o", linestyle="-", color="blue"
    )  # Изменяем стиль линий и маркеры

    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.title(f"График цены")  # Добавляем заголовок

    plt.xticks(rotation=45)  # Поворачиваем метки оси X для лучшей читаемости

    plt.grid(True)  # Добавляем сетку для лучшей ориентации

    plt.tight_layout()  # Улучшаем расположение элементов графика

    plt.savefig(f"png_temp/plot{index_img}.png")

    index_img += 1

    return f"png_temp/plot{index_img - 1}.png"


def get_info_about_coin_to_user(
    coin, cursor, conn
):  # при нажатии на кнопку коина пользователем выполняется это

    cursor.execute(f"SELECT price FROM coins WHERE coin = ?", (coin,))
    rows = cursor.fetchall()
    prices = [float(row[0]) for row in rows]
    dates = [i + 1.0 for i in range(len(rows))]
    str = plot(prices, dates)  # вывод картинки графика
    return str


def insert_info_to_db(data, cursor, conn):  # заносим в бд coin-price
    coins = list()
    for coin in data["symbols"]:
        coins.append((coin["symbol"], coin["last"]))

    cursor.executemany("""INSERT INTO coins VALUES (?, ?)""", coins)

    conn.commit()
