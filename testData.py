
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, Base, Transaction

from helpers import getDbString

engine = create_engine(getDbString(), pool_recycle=3600)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
s = DBSession()

# Insert a Person in the person table
#
#node = TreeNode(name='rootnode')
#TreeNode(name='node1', parent=node)
#TreeNode(name='node3', parent=node)
#
#node2 = TreeNode(name='node2')
#TreeNode(name='subnode1', parent=node2)
## node.children['node2'] = node2
## TreeNode(name='subnode2', parent=node.children['node2'])
#
#session.add(node)
#session.commit()
#
#print("done")

u1 = User(handle='u1')
s.add(u1)
s.commit()

u2 = User(handle='u2', owner=u1)
s.add(u2)
s.commit()

u3 = User(handle='u3', owner=u1)
s.add(u3)
s.commit()

t1 = Transaction(amount=1, buyer=u2, seller=u1, user_sold=u3)
s.add(t1)
s.commit()

##Insert an Address in the address table
#new_address = Address(post_code='00000', person=new_person)
#session.add(new_address)
#session.commit()


