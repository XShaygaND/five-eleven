import dotenv
import json
from telebot import TeleBot, types
from telebot.handler_backends import ContinueHandling
from handlers import handle_member_status, handle_member_select
from datatypes import StatusCode, CallbackType

token = dotenv.get_key('.env', 'PRODUCTION_BOT_TOKEN')
bot = TeleBot(token)

inline_btn = types.InlineKeyboardButton

@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.members_selection)
def handle_member_select_callback(call):
    status = handle_member_select(call)
    cid = call.message.chat.id

    if status == StatusCode.members_created:
        bot.send_message(cid, 'خوش آمدید.')


@bot.message_handler(func=lambda message: True)
def check_member(message):
    status = handle_member_status(message)

    if status == StatusCode.members_unauthorized:
        bot.reply_to(message, 'Fuck off!')
        return
    
    elif status == StatusCode.members_exists:
        bot.reply_to(message, "بعضی از کاربران هنوز ثبت نام نکرده اند.")
        return
    
    elif status == StatusCode.members_full:
        return ContinueHandling()

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    buttons = []

    for member in status:
        query = json.dumps({
            'type': CallbackType.members_selection,
            'member': member,
        })
        member_btn = inline_btn(member, callback_data=query)
        buttons.append(member_btn)
    
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'لطفا نام خود را انتخاب کنید: ', reply_markup=markup)

bot.polling()
