from pydantic import BaseModel, ConfigDict

class Blog(BaseModel):
    title: str
    body: str

class Show_blog(BaseModel):
    title: str
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
    class Config:
        orm_mode = True
