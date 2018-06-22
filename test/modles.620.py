from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, ForeignKey, Column, Integer, String, DateTime
#from sqlalchemy import Table, MetaData
#from sqlalchemy.orm import scoped_session

from config import SQLALCHEMY_DATABASE_URI



engine =create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        if session
        session.rollback()
        raise
    finally:
        session.close()

#方法一
# metadata = MetaData()
# def init_db():
#     metadata.create_all(engine)
# def drop_db():
#     metadata.drop_all(engine)
# 方法二
Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)



# 公共表
# USER表
# 方法一:
# users = Table('user', metadata,
#     Column('id', String(16), Sequence('user_id_seq'), primary_key=True),  # 兼容性： String指定长度， 
#     Column('phone', String(16)),
#     Column('pwd', String(16)),
#     Column('dtTime', DateTime),
#     Column('status', Integer)
#     )
# 方法二:
class users(Base):
    __tablename__ = 'user'
    id = Column(String(16), Sequence('user_id_seq'), primary_key=True)
    phone = Column(String(16))
    pwd = Column(String(16))
    dtTime = Column(DateTime)
    status = Column(Integer)

    # 非必需
    def __repr__(self):
        return "<user>{}:{}".format(self.id, self.status)

