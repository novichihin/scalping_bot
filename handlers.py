import telebot
from telebot import types

# Список поддерживаемых криптовалют
CRYPTO_LIST = [
    "BTC",
    "ETH",
    "XRP",
    "LTC",
    "SOL",
]  # Можете дополнить этот список другими криптовалютами


# Функция для подключения обработчиков
def setup_handlers(bot):
    # Обработчик команды /start
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name}! Я бот для скальпинга криптовалют VSEVOLOD. "
            "Для начала выбери криптовалюту с помощью команды /select_crypto.",
        )

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
        bot.send_message(message.chat.id, "Выбери криптовалюту:", reply_markup=keyboard)

    # Обработчик выбора криптовалюты
    @bot.message_handler(func=lambda message: message.text in CRYPTO_LIST)
    def handle_crypto_selection(message):
        selected_crypto = message.text
        bot.send_message(
            message.chat.id, f"Ты выбрал {selected_crypto} для скальпинга!"
        )
