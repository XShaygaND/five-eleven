class StatusCode:
    members_full = 'members_full'
    members_exists = 'members_exists'
    members_unauthorized = 'members_unauthorized'
    members_created = 'members_created'

    requests_notfound = 'requests_notfound'
    requests_exists = 'requests_exists'

    expenses_needs_spender = 'expenses_needs_spender'


class CallbackType:
    members_selection = 'mem_sel'

    menu_expense_new = 'men_new'
    menu_expense_list = 'men_elist'
    menu_members_list = 'men_mlist'

    menu_expense_new_type = 'men_en_type'
    menu_expense_new_members = 'men_en_mems'
    menu_expense_new_members_toggle = 'men_en_mems_tog'
    menu_expense_new_spender = 'men_en_spender'

    menu_confirm = 'men_confirm'
    menu_cancel = 'men_cancel'


class RequestType:
    member_request = 'mem_req'

    menu_expense_new_request = 'men_en_req'
