def add_user_coin(name, coin, cursor, conn):
    user = name
    s = [(user, coin)]
    cursor.executemany('''INSERT INTO users VALUES (?, ?)''', s)
    conn.commit()


def get_all_users_coins(user, cursor):
    cursor.execute(f'SELECT coin FROM users WHERE name_user = ?', (user,))
    rows = cursor.fetchall()

    for row in rows:
        print(row[0])

    return rows