import os
import json
from datatypes import CallbackType, Permissions

## GENERAL ##

MEMBERS = ['Ali', 'Orod', 'Sina', 'Roham', 'Shahriar', 'Mamad']

OWNER_CID = 479147855
FINANCE_HANDLER = 'Ali'

MAX_EXPENSE_LIST = 20


## MENU ##

MENU_OPTIONS = {
    'new_expense': {'fa': 'ایجاد خرج', 'callback': json.dumps({'type': CallbackType.menu_expense_new}), 'solo': True, 'perms': [Permissions.admin]},
    'expense_list': {'fa': 'مشاهده مخارج', 'callback': json.dumps({'type': CallbackType.menu_expense_list}), 'solo': False, 'perms': [Permissions.admin, Permissions.member]},
    'members_list': {'fa': 'مشاهده اعضا', 'callback': json.dumps({'type': CallbackType.menu_members_list}), 'solo': False, 'perms': [Permissions.admin]},
}

MENU_NEW_EXPENSE = {
    'personal_card': {'fa': 'کارت شخصی', 'callback': json.dumps({'type': CallbackType.menu_expense_new_type, 'room': False})},
    'room_card': {'fa': 'کارت اتاق', 'callback': json.dumps({'type': CallbackType.menu_expense_new_type, 'room': True})},
}


## MEDIA ##

MEDIA_DIR = os.path.join(os.getcwd(), 'media\\')
DATABASE_DIR = 'db.json'