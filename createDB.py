from sqlalchemy.engine import create_engine
import sys
from configuration import friendBizConfig
from models import Base

platform = sys.argv[1] if len(sys.argv) > 1 else "dev"

print ("Creating schema in " + platform)

engine = create_engine(friendBizConfig.dbConnectionString[platform], pool_recycle=3600)

Base.metadata.create_all(engine)
