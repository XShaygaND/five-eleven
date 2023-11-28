import settings
from classes import Member
from datatypes import StatusCode
from telebot import types

def handle_member_status(message: types.Message):
    cid = message.chat.id
    
    if Member.count == 6:
        if Member.exists(cid):
            return StatusCode.members_full

        else:
            return StatusCode.members_unauthorized
    
    elif Member.exists(cid):
        return StatusCode.members_exists

    members = [member.lower() for member in settings.MEMBERS]

    return [member for member in Member.get_all() if member in members]
