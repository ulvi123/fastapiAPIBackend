from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # type: ignore
from sqlalchemy.sql.sqltypes import TIMESTAMP # type: ignore
from sqlalchemy.sql.expression import text # type: ignore
from sqlalchemy.orm import relationship

#Model class - this is creating a table in the postgres when we create a model

#Model for the post
class Post(Base):
    __tablename__ = "posts"
    id  = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", on_delete="CASCADE"), nullable=False) #referring to the User model id but using the table name instead of the class name
    owner = relationship("User") # fetch the User based on the owner_id and return
    
#Model for the User table in DB
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
#Model for the votes table DB
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id", on_delete="CASCADE"), primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id", on_delete="CASCADE"), primary_key=True)
    

