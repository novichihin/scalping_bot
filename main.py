import telebot
from handlers import setup_handlers
from dotenv import dotenv_values

# Создаем экземпляр бота, указывая токен
config = dotenv_values()
token = config["TOKEN"]
bot = telebot.TeleBot(token)

# Подключаем обработчики команд
setup_handlers(bot)

# Запускаем бота
bot.polling()
