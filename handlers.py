import sqlite3

import telebot
from telebot import types
import webbrowser

from scalping_infrasct import get_info_about_coin_to_user



# Список поддерживаемых криптовалют
CRYPTO_LIST = [
    "BTC",
    "ETH",
    "XRP",
    "LTC",
    "SOL",
]  # Можете дополнить этот список другими криптовалютами

CRYPTO_DICT = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "XRP": "ripple",
    "LTC": "litecoin",
    "SOL": "solana",
}

temp_base_users = []


def main_menu(bot, chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    list_button = types.InlineKeyboardButton(
        text="Просмотреть криптовалюты", request_poll="/list"
    )
    select_button = types.InlineKeyboardButton(
        text="Выбрать криптовалюту", request_poll="/select_crypto"
    )
    keyboard.add(list_button, select_button)
    bot.send_message(
        chat_id,
        "Выберите действие:",
        reply_markup=keyboard,
    )


# Функция для подключения обработчиков
def setup_handlers(bot):

    # Обработчик команды /start
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name}! Я бот для скальпинга криптовалют VSEVOLOD.\n\n"
            "Для начала выбери криптовалюту с помощью команды /select_crypto.",
        )
        main_menu(bot, message.chat.id)

    # Обработчик нажатия на кнопку "Просмотреть криптовалюты"
    @bot.message_handler(
        func=lambda message: message.text == "Просмотреть криптовалюты"
    )
    def handle_list_button(message):
        list(message)

    # Обработчик нажатия на кнопку "Выбрать криптовалюту"
    @bot.message_handler(func=lambda message: message.text == "Выбрать криптовалюту")
    def handle_select_button(message):
        select_crypto(message)

    # Обработчик команды /help
    @bot.message_handler(commands=["help"])
    def help(message):
        bot.send_message(
            message.chat.id,
            "Это бот для скальпинга криптовалют. "
            "Доступные команды:\n/select_crypto - выбрать криптовалюту для скальпинга\n/help - помощь",
        )

    # Обработчик команды /select_crypto
    @bot.message_handler(commands=["select_crypto"])
    def select_crypto(message):
        keyboard = telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        for crypto in CRYPTO_LIST:
            keyboard.add(crypto)
        bot.send_message(
            message.chat.id,
            "Выбери криптовалюту:",
            reply_markup=keyboard,
        )

    # Обработчик выбора криптовалюты
    @bot.message_handler(
        func=lambda message: message.text in CRYPTO_LIST
        and message.text not in temp_base_users
    )
    def handle_crypto_selection(message):
        selected_crypto = message.text
        if selected_crypto in temp_base_users:
            bot.send_message(
                message.chat.id,
                f"Ты уже добавил {selected_crypto} для скальпинга!/n Выбери что-то еще или переходи к выбору /list",
            )
        else:
            bot.send_message(
                message.chat.id, f"Ты выбрал {selected_crypto} для скальпинга!"
            )
            temp_base_users.append(selected_crypto)
            main_menu(bot, message.chat.id)

    # Добавляем новый обработчик команды для выбора из списка криптовалют
    @bot.message_handler(commands=["list"])
    def list(message):
        keyboard = telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        for crypto in temp_base_users:
            button = telebot.types.KeyboardButton(text=crypto)
            keyboard.add(button)
        bot.send_message(
            message.chat.id,
            "Выбери криптовалюту из списка:",
            reply_markup=keyboard,
        )

    # Обработчик выбора криптовалюты из списка выбранных пользователем
    @bot.message_handler(func=lambda message: message.text in temp_base_users)
    def handle_chosen_crypto(message):
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        selected_crypto = message.text
        bot.send_message(
            message.chat.id,
            f"Ты выбрал {selected_crypto} для просмотра детальной информации.",
        )
        # # Открываем сайт CoinMarketCap для выбранной криптовалюты
        # webbrowser.open(
        #     f"https://coinmarketcap.com/ru/currencies/{CRYPTO_DICT[selected_crypto]}/"
        # )
        with open(f'{get_info_about_coin_to_user(selected_crypto, cursor, conn)}', 'rb') as file:
            bot.send_photo(
                message.chat.id,
                photo=file,

            )
        main_menu(bot, message.chat.id)

    # Функция для создания InlineKeyboardMarkup
    def create_inline_keyboard(options):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text=crypto, callback_data=crypto)
            for crypto in options
        ]
        keyboard.add(*buttons)
        return keyboard

