from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title: str
    body: str    
    user_id : int

class UpdateBlog(BaseModel):
    title: str | None = ""
    body: str | None = ""


class User(BaseModel):
    name : str
    email : str
    password : str

class ShowUser(BaseModel):
    name : str
    email : str

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    user: ShowUser

    class Config:
        orm_mode = True