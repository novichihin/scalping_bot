import requests

def get_info_about_coin(coin):
    url = f"https://api.freecryptoapi.com/v1/getData?symbol=BTC+ETH"
    headers = {'Authorization': 'Bearer h77qb2uqo6a9956l6ssj'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error: API request failed with status code", response.status_code)



def insert_info_to_db(data, cursor, conn):
    coins = list()
    for coin in data['symbols']:
        coins.append((coin['symbol'], coin['last']))

    
    cursor.executemany('''INSERT INTO coins VALUES (?, ?)''', coins)

    conn.commit()