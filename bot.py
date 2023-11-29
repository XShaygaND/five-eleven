import dotenv
import json
import settings
from telebot import TeleBot, types
from telebot.handler_backends import ContinueHandling
from handlers import handle_member_status, handle_member_select, handle_menu_command
from datatypes import StatusCode, CallbackType

token = dotenv.get_key('.env', 'PRODUCTION_BOT_TOKEN')
bot = TeleBot(token)

inline_btn = types.InlineKeyboardButton

@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.members_selection)
def handle_member_select_callback(call):
    status = handle_member_select(call)
    cid = call.message.chat.id

    if status == StatusCode.members_created:
        markup = types.ReplyKeyboardMarkup()
        mid = call.message.message_id

        bot.edit_message_text('خوش آمدید.', cid, mid, reply_markup=markup)
    
    elif status == StatusCode.members_exists:
        markup = types.ReplyKeyboardMarkup()
        mid = call.message.message_id

        bot.edit_message_text('این کاربر قبلا ثبت نام کرده است.', cid, mid, reply_markup=markup)
    
    elif status == StatusCode.requests_notfound:
        markup = types.ReplyKeyboardMarkup()
        mid = call.message.message_id

        bot.edit_message_text('خطا: درخواست شما یافت نشد!', cid, mid, reply_markup=markup)


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


@bot.message_handler(commands=['menu'])
def send_menu(message):
    status = handle_menu_command(message)

    if status == StatusCode.members_unauthorized:
        bot.reply_to(message, f'مدیر مخارج {settings.FINANCE_HANDLER} است.')

        return
    
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    buttons = []

    for option in status:
        button = inline_btn(option['fa'], callback_data=option['callback'])

        if option['solo']:
            markup.add(button)

        else:
            buttons.append(button)
        
    markup.add(*buttons)
    
    bot.send_message(message.chat.id, 'انتخاب کنید:', reply_markup=markup)



bot.polling()
