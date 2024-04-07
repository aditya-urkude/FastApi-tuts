from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship("Blogs", back_populates="creator")

class Blogs(Base):
    __tablename__ = "Blog_table"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("Users", back_populates="blogs")