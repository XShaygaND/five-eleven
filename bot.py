from telebot import TeleBot
import dotenv

token = dotenv.get_key('.env', 'PRODUCTION_BOT_TOKEN')
bot = TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'hi')
