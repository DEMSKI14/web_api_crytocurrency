import requests
import json
import sqlite3
from win10toast import ToastNotifier


def get_crypto_data(api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None


def save_data_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def print_crypto_info(data):
    for crypto in data['data']:
        name = crypto['name']
        symbol = crypto['symbol']
        price = crypto['quote']['USD']['price']
        print(f"Name: {name}")
        print(f"Symbol: {symbol}")
        print(f"Price: {price}")
        print("---------------------")


def create_database_table():
    conn = sqlite3.connect('crypto.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cryptocurrencies
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 symbol TEXT,
                 price REAL)''')
    conn.commit()
    conn.close()


def insert_data_into_database(data):
    conn = sqlite3.connect('crypto.db')
    c = conn.cursor()
    for crypto in data['data']:
        name = crypto['name']
        symbol = crypto['symbol']
        price = crypto['quote']['USD']['price']
        c.execute("INSERT INTO cryptocurrencies (name, symbol, price) VALUES (?, ?, ?)", (name, symbol, price))
    conn.commit()
    conn.close()

def show_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message)

api_key = "b5048026-876e-468a-94c8-4efec6d4daa0"
data = get_crypto_data(api_key)

if data is not None:
    save_data_to_json(data, 'crypto_data.json')
    print_crypto_info(data)

    create_database_table()
    insert_data_into_database(data)

    show_notification("Crypto Data", "წარმატებით განხორციელდა.")
else:
    print("დაფიქსირდა შეცდომა.")
