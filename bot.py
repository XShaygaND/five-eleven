import dotenv
from telebot import TeleBot
from telebot.handler_backends import ContinueHandling
from handlers import handle_member_status
from datatypes import StatusCode

token = dotenv.get_key('.env', 'PRODUCTION_BOT_TOKEN')
bot = TeleBot(token)

@bot.message_handler(lambda message: True)
def check_member(message):
    status = handle_member_status(message)

    if status == StatusCode.members_unauthorized:
        bot.reply_to(message, 'Fuck off!')
        return
    
    elif status == StatusCode.members_exists:
        bot.reply_to(message, 'These users havent registered yet:')
        #TODO: add members
        return
    
    elif status == StatusCode.members_full:
        return ContinueHandling()

    #TODO: ask user and register
