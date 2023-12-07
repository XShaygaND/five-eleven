from tinydb import TinyDB, Query
from typing import List, Dict, Union
from settings import MEDIA_DIR, DATABASE_DIR

db = TinyDB('{}{}'.format(MEDIA_DIR, DATABASE_DIR))
members = db.table('members')
requests = db.table('requests')
expenses = db.table('expenses')

def get_member_query(cid: int):
    Member = Query()

    return members.get(Member.cid==cid)


def get_all_members_query():
    
    return members.all()


def get_member_count():
    return len(members.all())


def save_member(cid: int, name: str, balance: int):
    query = {
        'cid': cid,
        'name': name,
        'balance': balance,
    }

    return members.insert(query)


def update_member(id: int, cid: int, name: str, balance: int):
    query = {
        'cid': cid,
        'name': name,
        'balance': balance,
    }

    return members.update(query, doc_ids=[id])


def get_request_query(type: str, cid: int):
    Request = Query()
    requestq = requests.get(cond=(Request.type==type) & (Request.cid==cid))

    return requestq


def save_request(type: str, cid: int, mlist: List[List[int]], kwargs: Dict):
    query = {
        'type': type,
        'cid': cid,
        'mlist': mlist,
        'kwargs': kwargs,
    }

    return requests.insert(query)


def update_request(id: int, type: str, cid: int, mlist: List[Dict[int, int]], kwargs: Dict):
    query = {
        'type': type,
        'cid': cid,
        'mlist': mlist,
        'kwargs': kwargs,
    }

    return requests.update(query, doc_ids=[id])


def delete_request(id: int, type: str, cid: int, mlist: List[Dict[int, int]], kwargs: Dict):
    query = {
        'type': type,
        'cid': cid,
        'mlist': mlist,
        'kwargs': kwargs,
    }

    return requests.remove(query, doc_ids=[id])


def get_expense_query(id: int):
    return expenses.get(doc_id=id)


def get_all_expenses_query():
    return expenses.all()


def save_expense(amount: int, reason: str, spender: Union[str, None], members: list):
    query = {
        'amount': amount,
        'reason': reason,
        'spender': spender,
        'members': members,
    }

    return expenses.insert(query)


def update_expense(id: int, amount: int, reason: str, spender: Union[str, None], members: list):
    query = {
        'amount': amount,
        'reason': reason,
        'spender': spender,
        'members': members,
    }

    return expenses.update(query, doc_ids=[id])


def delete_expense(id: int):
    return expenses.remove(doc_ids=[id])
