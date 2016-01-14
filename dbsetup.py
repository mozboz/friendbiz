from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import Base

from models import User, Transaction

engine = create_engine('mysql+mysqldb://twitfriends:monkey@localhost/twitfriends', pool_recycle=3600)

Base.metadata.create_all(engine)
