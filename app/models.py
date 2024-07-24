from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Relationship
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    Publised = Column(Boolean,server_default='True')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = Relationship("USer")

class USer(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    phone_number = Column(String,nullable=False,unique=True)
    Email = Column(String,nullable=False,unique=True)
    Password = Column(String,nullable=False)
    username = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))



class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    