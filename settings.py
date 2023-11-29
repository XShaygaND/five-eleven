import os
import json
from datatypes import CallbackType

## GENERAL ##

MEMBERS = ['Ali', 'Orod', 'Sina', 'Roham', 'Shahriar', 'Mamad']
OWNER_CID = 479147855
FINANCE_HANDLER = 'Ali'
MENU_OPTIONS = {
    'new_expense': {'fa': 'ایجاد خرج', 'callback': json.dumps({'type': CallbackType.menu_new}), 'solo': True},
    'expense_list': {'fa': 'مشاهده مخارج', 'callback': json.dumps({'type': CallbackType.menu_expense_list}), 'solo': False},
    'members_list': {'fa': 'مشاهده اعضا', 'callback': json.dumps({'type': CallbackType.menu_members_list}), 'solo': False},
}


## MEDIA ##

MEDIA_DIR = os.path.join(os.getcwd(), 'media\\')
DATABASE_DIR = 'db.json'