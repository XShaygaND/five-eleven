import dotenv
import json
import settings
import threading
from typing import Optional, Union
from telebot import TeleBot, types
from telebot.handler_backends import ContinueHandling
from handlers import handle_member_status, handle_member_select, handle_menu_command, handle_new_expense_request, handle_new_expense_request_type, handle_new_expense_request_amount
from handlers import handle_new_expense_request_member_toggle, handle_new_expense_request_members_confirm, handle_new_expense_request_spender, handle_new_expense_request_reason
from handlers import handle_expense_menu_request, handle_expense_details_request
from datatypes import StatusCode, CallbackType

token = dotenv.get_key('.env', 'PRODUCTION_BOT_TOKEN')
bot = TeleBot(token)

lock = threading.Lock()

inline_btn = types.InlineKeyboardButton

@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.members_selection)
def handle_member_select_callback(call):
    with lock:
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


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.menu_expense_new)
def handle_new_expense_menu(call):
    with lock:
        cid = call.message.chat.id
        mid = call.message.message_id

        status = handle_new_expense_request(call)

        if status == StatusCode.requests_exists:
            bot.send_message(cid, 'شما یک درخواست باز دارید.')
            return

        markup = types.ForceReply(input_field_placeholder='مبلغ')

        msg = bot.send_message(cid, 'لطفا مبلغ خرج را بنویسید:', reply_markup=markup)
        bot.delete_message(cid, mid)

        bot.register_next_step_handler(msg, check_amount, args=[msg.message_id])


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.menu_expense_new_type)
def handle_new_expense_menu_type(call):
    with lock:
        status = handle_new_expense_request_type(call)
        cid = call.message.chat.id
        mid = call.message.message_id

        if status == StatusCode.requests_notfound:
            bot.send_message(cid, 'خطا: درخواست شما یافت نشد!')

        elif not status:
            send_members_menu(CallbackType.menu_expense_new_spender, cid, mid)
            
        else:
            send_expense_member_toggle_menu(cid, mid)


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] in [CallbackType.menu_expense_new_members_toggle, CallbackType.menu_confirm])
def handle_new_expense_request_menu_member_toggle(call):
    with lock:
        query = json.loads(call.data)
        cid = call.message.chat.id
        mid = call.message.message_id

        if query['type'] == CallbackType.menu_expense_new_members_toggle:
            member = query['member']
            status = handle_new_expense_request_member_toggle(call)

            if status == StatusCode.requests_notfound:
                bot.send_message(cid, 'خطا: درخواست شما یافت نشد!')
            
            else:
                send_expense_member_toggle_menu(cid, mid, status)

        elif query['type'] == CallbackType.menu_confirm:
            status = handle_new_expense_request_members_confirm(call)
            cid = call.message.chat.id
            mid = call.message.message_id

            if status == StatusCode.requests_notfound:
                bot.send_message(cid, 'خطا: درخواست شما یافت نشد!')
            
            else:
                send_expense_to_members(status)
                send_main_menu(cid, mid)

        
@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.menu_expense_new_spender)
def handle_new_expense_request_menu_spender(call):
    with lock:
        cid = call.message.chat.id
        mid = call.message.message_id

        status = handle_new_expense_request_spender(call)

        if status == StatusCode.requests_notfound:
                bot.send_message(cid, 'خطا: درخواست شما یافت نشد!')

        else:
                send_expense_member_toggle_menu(cid, mid)
    

@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.menu_expense_list)
def handle_expense_list_menu(call):
    with lock:
        cid = call.message.chat.id
        mid = call.message.message_id

        expenses = handle_expense_menu_request(call)

        send_expense_list_menu(expenses, cid, mid)


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.menu_expense_details)
def handle_expense_details(call):
    with lock:
        cid = call.message.chat.id
        mid = call.message.message_id
        id = json.loads(call.data)['id']

        details = handle_expense_details_request(call)
        details['id'] = id
        details['members'] = ' '.join(details['members'])
        details['spender'] = details['spender'] if details['spender'] else 'اتاق'

        send_expense_details_menu(details, cid, mid)

    
@bot.callback_query_handler(func=lambda call: json.loads(call.data)['type'] == CallbackType.menu_expense_edit)
def handle_expense_edit(call):
    with lock:
        pass


@bot.message_handler(func=lambda message: True)
def check_member(message):
    with lock:
        status = handle_member_status(message)
        cid = message.chat.id
        mid = message.message_id

        bot.delete_message(cid, mid)

        if status == StatusCode.members_unauthorized:
            bot.reply_to(message, 'Fuck off!')
            return
        
        elif status == StatusCode.members_exists:
            bot.reply_to(message, "بعضی از کاربران هنوز ثبت نام نکرده اند.")
            return
        
        elif status == StatusCode.members_full:
            return ContinueHandling()

        send_members_menu(CallbackType.members_selection, cid)


@bot.message_handler(commands=['menu'])
def send_menu(message):
    with lock:
        status = handle_menu_command(message)
        cid = message.chat.id
        mid = message.message_id

        if status == StatusCode.members_unauthorized:
            bot.reply_to(message, f'مدیر مخارج {settings.FINANCE_HANDLER} است.')

            return

        send_main_menu(cid)


def send_main_menu(cid: int, mid: Optional[int] = None):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    buttons = []

    for option in settings.MENU_OPTIONS:
        option = settings.MENU_OPTIONS[option]
        button = inline_btn(option['fa'], callback_data=option['callback'])

        if option['solo']:
            markup.add(button)

        else:
            buttons.append(button)
        
    markup.add(*buttons)
    
    if not mid:
        bot.send_message(cid, 'انتخاب کنید:', reply_markup=markup)
    
    else:
        bot.edit_message_text('انتخاب کنید:', cid, mid, reply_markup=markup)

    
def send_members_menu(type: CallbackType, cid: int, mid: Optional[int] = None): #TODO: add permission filtered menus
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    buttons = []

    for member in settings.MEMBERS:
        query = json.dumps({
            'type': type,
            'member': member,
        })
        member_btn = inline_btn(member, callback_data=query)
        buttons.append(member_btn)
    
    markup.add(*buttons)

    text_msg = 'لطفا نام خود را انتخاب کنید:' if type == CallbackType.members_selection else 'لطفا شخصی که خرج کرده را انتخاب کنید:'

    if not mid:
        bot.send_message(cid, text_msg, reply_markup=markup)
    
    else:
        bot.edit_message_text(text_msg, cid, mid, reply_markup=markup)


def send_expense_type_menu(cid: int, mid: Optional[int] = None):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1

    buttons = []

    for option in settings.MENU_NEW_EXPENSE:
        option = settings.MENU_NEW_EXPENSE[option]
        button = inline_btn(option['fa'], callback_data=option['callback'])
        buttons.append(button)
        
    markup.add(*buttons)

    if not mid:
        bot.send_message(cid, 'لطفا یک حالت را انتخاب کنید:', reply_markup=markup)
    
    else:
        bot.edit_message_text('لطفا یک حالت را انتخاب کنید:', cid, mid, reply_markup=markup)


def send_expense_member_toggle_menu(cid: int, mid: Optional[int] = None, members_list: Optional[list] = None):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    buttons = []
    confirm_button = inline_btn('Confirm ⚪', callback_data=json.dumps({'type': CallbackType.menu_confirm}))

    members = members_list if members_list else settings.MEMBERS

    for member in members:
        query = json.dumps({
            'type': CallbackType.menu_expense_new_members_toggle,
            'member': member['name'] if members_list else member,
        })
        
        active = member['active'] if members_list else False
        name = member['name'] if members_list else member

        icon = '✅' if active else '☑'
        member_btn = inline_btn((name + f' {icon}'), callback_data=query)
        buttons.append(member_btn)
    
    markup.add(*buttons)
    markup.add(confirm_button)

    if not mid:
        bot.send_message(cid, 'لطفا کاربرانی که در خرج شریک اند را انتخاب کنید:', reply_markup=markup)
    
    else:
        bot.edit_message_text('لطفا کاربرانی که در خرج شریک اند را انتخاب کنید:', cid, mid, reply_markup=markup)

    
def send_expense_list_menu(expenses: list, cid: int, mid: Optional[int] = None):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    buttons = []

    i = 0

    for expense in expenses:
        if not i < 20:
            break

        text = str(expenses[expense]['amount']) + ' | ' + expenses[expense]['reason']
        query = json.dumps({
            'type': CallbackType.menu_expense_details,
            'id': expense,
        })

        expense_btn = inline_btn(text, callback_data=query)
        buttons.append(expense_btn)

        i += 1 #TODO: better code fix this

    markup.add(*buttons)

    if not mid:
        bot.send_message(cid, 'لطفا یک خرج را انتخاب کنید:', reply_markup=markup)
    
    else:
        bot.edit_message_text('لطفا یک خرج را انتخاب کنید:', cid, mid, reply_markup=markup)


def send_expense_details_menu(details: dict, cid: int, mid: Optional[int] = None):
    fa = {
        'amount': 'مبلغ',
        'reason': 'علت',
        'spender': 'مخرج',
        'members': 'اعضا',
    }

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    buttons = []
    text = ''

    for detail in details:
        if detail == 'id': #TODO: bruh
            continue

        query = json.dumps({
            'type': CallbackType.menu_expense_edit,
            'id': details['id'],
            'action': detail,
        })

        text += fa[detail] + ': ' + str(details[detail]) + '\n'
        buttons.append(inline_btn(fa[detail], callback_data=query))

    markup.add(*buttons)

    text += 'یکی از موارد را برای ویرایش انتخاب کنید:'

    if not mid:
        bot.send_message(cid, text, reply_markup=markup)
        
    else:
        bot.edit_message_text(text, cid, mid, reply_markup=markup)



def check_amount(message, args):
    amount = message.text
    cid = message.chat.id
    mid = message.message_id
    orig_mid = args[0]

    bot.delete_message(cid, mid)

    if not amount.isdigit():
        msg = bot.send_message(cid, 'مبلغ باید حتما یک عدد باشد:')
        bot.register_next_step_handler(msg, check_amount)

    else:
        status = handle_new_expense_request_amount(message)

        if status == StatusCode.requests_notfound:
            bot.send_message(cid, 'خطا: درخواست شما یافت نشد!')

        else:
            markup = types.ForceReply(input_field_placeholder='علت')

            msg = bot.send_message(cid, 'لطفا علت خرج را بنویسید:', reply_markup=markup)

            bot.register_next_step_handler(msg, check_reason, args=[msg.message_id])

            bot.delete_message(cid, orig_mid)


def check_reason(message, args):
    reason = message.text
    cid = message.chat.id
    mid = message.message_id
    orig_mid = args[0]

    bot.delete_message(cid, mid)

    if reason.isdigit():
        msg = bot.send_message(cid, 'دلیل نمیتواند عدد باشد:')
        bot.register_next_step_handler(msg, check_reason)
    
    else:
        status = handle_new_expense_request_reason(message)

        if status == StatusCode.requests_notfound:
            bot.send_message(cid, 'خطا: درخواست شما یافت نشد!')

        else:
            send_expense_type_menu(cid)

            bot.delete_message(cid, orig_mid)


def send_expense_to_members(query: dict):
    for member in query:
        message = '\n'.join([
            'تراکنش جدید', 'علت: ' + query[member]['reason'],
            'مبلغ: ' + per_num_format(query[member]['amount']),
            'موجودی شما: '+ per_num_format(query[member]['balance']),
        ])

        bot.send_message(
            member,
            message,
            )


def per_num_format(number: int):
    if number >= 0:
        return str(number)
    else:
        return str(abs(number)) + '-'


if __name__ == '__main__':
    bot.polling()
