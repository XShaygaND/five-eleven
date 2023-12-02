import os
import json
from datatypes import CallbackType

## GENERAL ##

MEMBERS = ['Ali', 'Orod', 'Sina', 'Roham', 'Shahriar', 'Mamad']

OWNER_CID = 479147855
FINANCE_HANDLER = 'Ali'


## MENU ##

MENU_OPTIONS = {
    'new_expense': {'fa': 'ایجاد خرج', 'callback': json.dumps({'type': CallbackType.menu_expense_new}), 'solo': True},
    'expense_list': {'fa': 'مشاهده مخارج', 'callback': json.dumps({'type': CallbackType.menu_expense_list}), 'solo': False},
    'members_list': {'fa': 'مشاهده اعضا', 'callback': json.dumps({'type': CallbackType.menu_members_list}), 'solo': False},
}

MENU_NEW_EXPENSE = {
    'personal_card': {'fa': 'کارت شخصی', 'callback': json.dumps({'type': CallbackType.menu_expense_new_type, 'room': False})},
    'room_card': {'fa': 'کارت اتاق', 'callback': json.dumps({'type': CallbackType.menu_expense_new_type, 'room': True})},
}


## MEDIA ##

MEDIA_DIR = os.path.join(os.getcwd(), 'media\\')
DATABASE_DIR = 'db.json'