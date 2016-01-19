from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sys
from models import Base

from models import User
from helpers import getDbString

platform = sys.argv[1] if len(sys.argv) > 1 else "dev"

print ("Creating schema in " + platform)

engine = create_engine(getDbString(platform), pool_recycle=3600)

Base.metadata.create_all(engine)
