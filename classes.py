from storage import get_member_query, get_all_members_query, get_member_count, save_member, update_member
from storage import get_request_query, save_request, update_request, delete_request
from datatypes import RequestType
from typing import List, Dict

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
    
    def exists(cid: int):
        return bool(get_member_query(cid))
    
    def count():
        return get_member_count()
    

class Request:

    def __init__(self, type: RequestType, cid: int, mlist: List[Dict[int, int]] = None, kwargs: Dict = None):
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
        self.mlist.append({cid: mid})
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

#TODO: add Expense
