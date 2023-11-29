from storage import get_member_query, get_all_members_query, get_member_count, save_member, update_member


class Member:
    
    count = get_member_count()


    def __init__(self, id: int = None, cid:int = None, name: str = None, balance: int = None):
        self.id = id
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
                id=memberq.doc_id,
                cid=memberq['cid'],
                name=memberq['name'],
                balance=memberq['balance'],
            )
        
        return member
    
    def get_all():
        membersq = get_all_members_query()
        members = []

        for memberq in membersq:
            members.append(Member(
                id=memberq.doc_id,
                cid=memberq['cid'],
                name=memberq['name'],
                balance=memberq['balance'],
            ))

        return members
    
    def exists(cid: int):
        return bool(get_member_query(cid))
    

#TODO: add Request
#TODO: add Expense
