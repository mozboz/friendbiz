
from models import User, Transaction

def setupUsers(session):
    u1 = User(handle='u1')
    session.add(u1)
    session.commit()
    
    u2 = User(handle='u2', owner=u1)
    session.add(u2)
    session.commit()
    
    u3 = User(handle='u3', owner=u1)
    session.add(u3)
    session.commit()
    
    t1 = Transaction(amount=1, buyer=u2, seller=u1, user_sold=u3)
    session.add(t1)
    session.commit()

    return u1, u2, u3, t1
##Insert an Address in the address table
#new_address = Address(post_code='00000', person=new_person)
#session.add(new_address)
#session.commit()


