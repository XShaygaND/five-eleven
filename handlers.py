import json
import settings
from classes import Member, Request, Expense
from datatypes import StatusCode, RequestType
from telebot import types

def handle_member_status(message: types.Message):
    cid = message.chat.id
    
    if Member.count() == len(settings.MEMBERS):
        if Member.exists(cid) or cid == settings.OWNER_CID:
            return StatusCode.members_full

        else:
            return StatusCode.members_unauthorized
    
    elif Member.exists(cid):
        return StatusCode.members_exists

    mid = message.message_id
    request = Request(type=RequestType.member_request, cid=cid, mlist=[cid, mid])
    request.save()

    return [member for member in settings.MEMBERS if member.lower() not in [member.name.lower() for member in Member.get_all()]]


def handle_member_select(call: types.CallbackQuery):
    query = json.loads(call.data)
    cid = call.message.chat.id

    if not Request.exists(RequestType.member_request, cid):
        return StatusCode.requests_notfound

    elif Member.exists(cid):
        request = Request.get(RequestType.member_request, cid)
        request.delete()

        return StatusCode.members_exists
    
    request = Request.get(RequestType.member_request, cid)
    request.delete()

    member = Member(cid=cid, name=query['member'], balance=0)
    member.save()

    return StatusCode.members_created


def handle_menu_command(message: types.Message):
    cid = message.chat.id
    name = Member.get(cid).name

    if name != settings.FINANCE_HANDLER and cid != settings.OWNER_CID:
        return StatusCode.members_unauthorized


def handle_new_expense_request(call: types.CallbackQuery):
    cid = call.message.chat.id

    if Request.exists(RequestType.menu_expense_new_request, cid):
        return StatusCode.requests_exists

    request = Request(RequestType.menu_expense_new_request, cid, [], {'members': []})
    request.save()


def handle_new_expense_request_type(call: types.CallbackQuery):
    query = json.loads(call.data)
    cid = call.message.chat.id

    if not Request.exists(RequestType.menu_expense_new_request, cid):
        return StatusCode.requests_notfound
    
    request = Request.get(RequestType.menu_expense_new_request, cid)
    request.kwargs['room'] = query['room']
    request.update()

    return query['room']


def handle_new_expense_request_amount(message: types.Message):
    amount = int(message.text)
    cid = message.chat.id

    if not Request.exists(RequestType.menu_expense_new_request, cid):
        return StatusCode.requests_notfound
    
    request = Request.get(RequestType.menu_expense_new_request, cid)
    request.kwargs['amount'] = amount
    request.update()


def handle_new_expense_request_reason(message: types.Message):
    reason = message.text
    cid = message.chat.id

    if not Request.exists(RequestType.menu_expense_new_request, cid):
        return StatusCode.requests_notfound

    request = Request.get(RequestType.menu_expense_new_request, cid)
    request.kwargs['reason'] = reason
    request.update()


def handle_new_expense_request_member_toggle(call: types.CallbackQuery):
    query = json.loads(call.data)
    cid = call.message.chat.id

    if not Request.exists(RequestType.menu_expense_new_request, cid):
        return StatusCode.requests_notfound
    
    member = query['member']

    request = Request.get(RequestType.menu_expense_new_request, cid)
    member_inlist = member in request.kwargs['members']


    if not member_inlist:
        request.kwargs['members'].append(member)
    
    else:
        request.kwargs['members'].remove(member)
    
    request.update()

    return [{'name': member, 'active': member in request.kwargs['members']} for member in settings.MEMBERS]


def handle_new_expense_request_members_confirm(call: types.CallbackQuery):
    cid = call.message.chat.id

    if not Request.exists(RequestType.menu_expense_new_request, cid):
        return StatusCode.requests_notfound
    
    request = Request.get(RequestType.menu_expense_new_request, cid)
    amount = request.kwargs['amount']
    reason = request.kwargs['reason']
    spender = request.kwargs['room']
    members = request.kwargs['members']

    expense = Expense(amount, reason, members, None if spender == True else spender)
    expense.save()

    request.delete()

    return handle_expense(expense)
    

def handle_new_expense_request_spender(call: types.CallbackQuery):
    cid = call.message.chat.id

    if not Request.exists(RequestType.menu_expense_new_request, cid):
        return StatusCode.requests_notfound
    
    request = Request.get(RequestType.menu_expense_new_request, cid)
    spender = json.loads(call.data)['member'] #TODO: check if spender is in members

    request.kwargs['room'] = spender
    request.update()

    
def handle_expense(expense: Expense):
    share = expense.amount / len(expense.members)
    members = {}

    for name in expense.members:
        member = Member.get_by_name(name)
        member.balance -= share
        member.update()

        amount = get_amount(expense, member)
        
        members[member.cid] = {
            'amount': amount,
            'reason': expense.reason,
            'balance': member.balance,
        }

    if expense.spender:
        member = Member.get_by_name(expense.spender)
        member.balance += expense.amount
        member.update()

        amount = get_amount(expense, member)
        
        members[member.cid] = {
            'amount': amount, #fix spender
            'reason': expense.reason,
            'balance': member.balance,
        }

    return members


def get_amount(expense: Expense, member: Member): #TODO: make this handle everything
    share = expense.amount / len(expense.members)
    spender = expense.spender

    if str(member) == spender:
        amount = expense.amount - share
    
    else:
        amount = -share

    return amount
