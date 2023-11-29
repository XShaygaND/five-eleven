import json
import settings
from classes import Member
from datatypes import StatusCode
from telebot import types

def handle_member_status(message: types.Message):
    cid = message.chat.id
    
    if Member.count == 6:
        if Member.exists(cid) or cid == settings.OWNER_CID:
            return StatusCode.members_full

        else:
            return StatusCode.members_unauthorized
    
    elif Member.exists(cid):
        return StatusCode.members_exists

    return [member for member in settings.MEMBERS if member not in [member.name.lower() for member in Member.get_all()]]


def handle_member_select(call: types.CallbackQuery):
    #TODO: add requests
    #TODO: handle better
    query = json.loads(call.data)
    cid = call.message.chat.id

    member = Member(cid=cid, name=query['member'], balance=0)
    member.save()

    return StatusCode.members_created
