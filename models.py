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
    owner_id = Column(Integer, ForeignKey(id), nullable=True)
    price = Column(Integer, nullable=False, default=1)
    balance = Column(Integer, nullable=False, default=0)

    inventory = relationship("User",
        cascade="all, delete-orphan",
        backref=backref('owner', remote_side=id)
        )

    transactions = relationship("TransactionLogItem",
        primaryjoin="or_(User.id==TransactionLogItem.seller_id, User.id==TransactionLogItem.buyer_id)",
        lazy = "dynamic",
        order_by = "desc(TransactionLogItem.time)"
    )

    def __repr__(self):
        return "<User(id='%s', handle='%s', owner='%s', balance='%s')>" % (
            self.id, self.handle, self.owner_id, self.balance)


class TransactionLogItem(Base):
    __tablename__ = 'transactionlog'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), default=datetime.utcnow)
    buyer_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # @todo there may not be a seller, change nullable
    seller_id = Column(Integer, ForeignKey('user.id'))
    user_sold_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    amount = Column(Integer)
    description = Column(String(1000), nullable=True)
    status = Column(String(250), nullable=False)
    reason = Column(String(250), nullable=True)
    buyer = relationship(User, foreign_keys=[buyer_id])
    seller = relationship(User, foreign_keys=[seller_id])
    user_sold = relationship(User, foreign_keys=[user_sold_id])

    def __repr__(self):
        return "<TransactionLogItem(id='%s', time='%s', buyer='%s', seller='%s', user_sold='%s', status='%s', amount='%s', description='%s')>" % (
            self.id, self.time, self.buyer_id, self.seller_id, self.user_sold_id, self.status, self.amount, self.description)

    # seller = relationship(User, back_populates="transactions_as_buyer", foreign_keys=[buyer_id])

    # user_id = Column(Integer, ForeignKey('user.id'))
