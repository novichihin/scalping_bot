def add_user_coin(name, coin, cursor, conn):  # добавляем в таблицу user-coin
    user = name
    s = [(user, coin, name)]
    cursor.executemany("""INSERT INTO users VALUES (?, ?, ?)""", s)
    conn.commit()


def get_all_users_coins(user, cursor):  # получаем все coins user`а
    cursor.execute(f"SELECT coin FROM users WHERE name_user = ?", (user,))
    rows = cursor.fetchall()

    for row in rows:
        print(row[0])

    return rows
