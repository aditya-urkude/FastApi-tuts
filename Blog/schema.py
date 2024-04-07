from pydantic import BaseModel, ConfigDict
from typing import List

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config:
        orm_mode = True

class User(BaseModel):
    name : str
    email : str
    password: str

class Show_user(BaseModel):
    # specific data to show
    name: str
    email: str
    blogs: List[Blog] = []
    class Config:
        orm_mode = True


class Show_blog(BaseModel):
    title: str
    creator : Show_user
    class Config:
        orm_mode = True
