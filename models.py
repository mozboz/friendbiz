from datetime import datetime
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql.expression import null
from sqlalchemy.types import Boolean, DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    handle = Column(String(250), nullable=False)
    owned = Column(Boolean(), default=False)
    owner_id = Column(Integer, ForeignKey(id), nullable=True)
    current_price = Column(Integer, nullable=False, default=1)
    balance = Column(Integer, nullable=False, default=0)

    owner_relationship = relationship("User",
        cascade="all, delete-orphan",
        backref=backref('owner', remote_side=id)
        )

    # transactions = relationship("Transaction")



class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), default=datetime.utcnow)
    buyer_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_sold_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    amount = Column(Integer)
    buyer = relationship(User, foreign_keys=[buyer_id])
    seller = relationship(User, foreign_keys=[seller_id])
    user_sold = relationship(User, foreign_keys=[user_sold_id])

    # seller = relationship(User, back_populates="transactions_as_buyer", foreign_keys=[buyer_id])

    # user_id = Column(Integer, ForeignKey('user.id'))




#class TreeNode(Base):
#    __tablename__ = 'tree'
#    id = Column(Integer, primary_key=True)
#    parent_id = Column(Integer, ForeignKey(id), nullable=True)
#    name = Column(String(50), nullable=False)
#
#    children = relationship("TreeNode",
#
#        # cascade deletions
#        cascade="all, delete-orphan",
#
#        # many to one + adjacency list - remote_side
#        # is required to reference the 'remote'
#        # column in the join condition.
#        backref=backref("parent", remote_side=id),
#
#        # children will be represented as a dictionary
#        # on the "name" attribute.
#        # collection_class=attribute_mapped_collection('name'),
#    )


#class Transaction(Base):
#    __tablename__ = 'transaction'
#    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
#    # Here we define columns for the table address.
#    # Notice that each column is also a normal Python instance attribute.
#    id = Column(Integer, primary_key=True)
#    time = Column(DateTime(timezone=True), default=datetime.utcnow)
#    buyer = Column(Integer, ForeignKey('user.id'))
#    seller = Column(Integer, ForeignKey('user.id'))
#    user_sold = Column(Integer, ForeignKey('user.id'))
#    amount = Column(Integer)
#    user = relationship("User")


# sqlalchemy.exc.ArgumentError: User.owner and back-reference User.owned_users are both of the same direction symbol('ONETOMANY').  Did you mean to set remote_side on the many-to-one side ?

