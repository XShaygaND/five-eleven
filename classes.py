from storage import get_member_query, get_all_members_query, get_member_count, save_member, update_member
from storage import get_request_query, save_request, update_request, delete_request
from storage import get_expense_query, save_expense, update_expense, delete_expense
from datatypes import RequestType
from typing import List, Dict, Union

class Member:

    def __init__(self, cid: int, name: str, balance: int):
        self.cid = cid
        self.name = name
        self.balance = balance

    def __str__(self):
        return self.name
    
    def save(self):
        return save_member(self.cid, self.name, self.balance)
    
    def update(self):
        return update_member(self.id, self.cid, self.name, self.balance)
    
    def get(cid: int):
        memberq = get_member_query(cid)
        member = []

        if memberq:
            member = Member(
                cid=memberq['cid'],
                name=memberq['name'],
                balance=memberq['balance'],
            )

            member.id = memberq.doc_id
        
        return member
    
    def get_all():
        membersq = get_all_members_query()
        members = []

        for memberq in membersq:
            member = Member(
                cid=memberq['cid'],
                name=memberq['name'],
                balance=memberq['balance'],
            )

            member.id = memberq.doc_id
            members.append(member)

        return members
    
    def get_by_name(name: str):
        return [member for member in Member.get_all() if member.name == name][0]
    
    def exists(cid: int):
        return bool(get_member_query(cid))
    
    def count():
        return get_member_count()
    

class Request:

    def __init__(self, type: RequestType, cid: int, mlist: List[List[int]] = None, kwargs: Dict = {}):
        self.type = type
        self.cid = cid
        self.mlist = mlist
        self.kwargs = kwargs
    
    def save(self):
        return save_request(self.type, self.cid, self.mlist, self.kwargs)
    
    def update(self):
        return update_request(self.id, self.type, self.cid, self.mlist, self.kwargs)
    
    def delete(self):
        return delete_request(self.id, self.type, self.cid, self.mlist, self.kwargs)

    def add_message(self, cid: int, mid: int):
        self.mlist.append([cid, mid])
        return self.update()

    def get(type: RequestType, cid: int):
        requestq = get_request_query(type, cid)
        request = []

        if requestq:
            request = Request(
                type=requestq['type'],
                cid=requestq['cid'],
                mlist=requestq['mlist'],
                kwargs=requestq['kwargs']
            )

            request.id = requestq.doc_id

        return request

    def exists(type: RequestType, cid: int):
        return bool(get_request_query(type, cid))


class Expense:

    def __init__(self, amount: int, reason: str, members: List[Member] = [], spender: Union[Member, None] = None):
        self.amount = amount
        self.reason = reason
        self.members = members
        self.spender = spender
    
    def save(self):
        return save_expense(self.amount, self.reason, self.members, self.spender)

    def update(self):
        return update_expense(self.id, self.amount, self.reason, self.members, self.spender)
    
    def delete(self):
        return delete_expense(self.id)
    
    def get(id: int):
        return get_expense_query(id)

#TODO: add room
#TODO: add deposit
