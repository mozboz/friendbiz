from sqlalchemy.orm import query
from models import User

__author__ = 'james'




def getInventory(userId, session):
    u1 = session.query(User).filter(User.id == userId).one()
    return u1.inventory


def getOwnerID(userId, session):
    u = session.query(User.owner_id).filter(User.id == userId).one()
    if u == False:
        return False
    else:
        return u.owner_id

