from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import Base

from models import User
from helpers import getDbString

engine = create_engine(getDbString(), pool_recycle=3600)

Base.metadata.create_all(engine)
