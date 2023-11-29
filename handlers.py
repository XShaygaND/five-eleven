import json
import settings
from classes import Member, Request
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
    request = Request(type=RequestType.member_request, cid=cid, mlist=[{cid: mid}])
    request.save()

    return [member for member in settings.MEMBERS if member.lower() not in [member.name.lower() for member in Member.get_all()]]


def handle_member_select(call: types.CallbackQuery):
    #TODO: add requests
    #TODO: handle better
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
    
    return [settings.MENU_OPTIONS[option] for option in settings.MENU_OPTIONS]
