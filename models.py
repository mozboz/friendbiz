from datetime import datetime
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
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
    owned = Column(Boolean())
    owner_id = Column(Integer, nullable=True, default=null)
    current_price = Column(Integer, nullable=False, default=1)
    balance = Column(Integer, nullable=False, default=0)

class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), default=datetime.utcnow)
    buyer = Column(Integer, ForeignKey('user.id'))
    seller = Column(Integer, ForeignKey('user.id'))
    user = Column(Integer, ForeignKey('user.id'))
    amount = Column(Integer)