import random
import string
from models import User, TransactionLogItem

def setupUsers(session, config):
    u1 = User(handle=id_generator(), price = config['startingPrice'], balance = config['startingBalance'])
    session.add(u1)
    session.commit()

    u2 = User(handle=id_generator(), owner=u1, price = config['startingPrice'], balance = config['startingBalance'])
    session.add(u2)
    session.commit()

    u3 = User(handle=id_generator(), owner=u1, price = config['startingPrice'], balance = config['startingBalance'])
    session.add(u3)
    session.commit()

    return u1, u2, u3

def setupUsersAndTransactions(session, config):

    u1, u2, u3 = setupUsers(session, config)

    t1 = TransactionLogItem(amount=1, buyer=u2, seller=u1, user_sold=u3, status=TransactionStatus.SUCCESS, description="setupUsers test transaction creation")
    session.add(t1)
    session.commit()

    t2 = TransactionLogItem(amount=1, buyer=u3, seller=u1, user_sold=u3, status=TransactionStatus.SUCCESS, description="setupUsers test transaction creation")
    session.add(t2)
    session.commit()

    return u1, u2, u3, t1


def setupBuyUsers(session, config):
    u1, u2, u3, t1 = setupUsersAndTransactions(session, config)

    u4 = User(handle=id_generator(), price = config['startingPrice'], balance = config['startingBalance'])
    session.add(u4)
    session.commit()

    return u1, u2, u3, u4

def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


