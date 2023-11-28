from tinydb import TinyDB, Query
from settings import MEDIA_DIR, DATABASE_DIR

db = TinyDB('{}{}'.format(MEDIA_DIR, DATABASE_DIR))
members = db.table('members')

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
