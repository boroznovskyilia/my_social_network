from pydantic import BaseModel,Field,EmailStr
import datetime
from typing import List,Optional
from posts.schema import PostInDb,MyPost
from chat.schema import MessageInDb,ChatInDb
from fastapi import Form

class User(BaseModel):
    username:str = Field(max_length=100)
    email:EmailStr
    class Config:
        from_attributes = True

class UserCreate(User):
    password:str = Field(min_length=3)

class UserUpdate(UserCreate):
    pass

class UserShow(User):
    date_create:datetime.datetime
    followers:Optional[List['User']]
    following:Optional[List['User']]
    posts:Optional[List['MyPost']]

class UserInDb(User):
    id: int  = Field(ge = 1)
    hashed_password:str = Field(min_length=4)
    date_create:datetime.datetime
    posts:Optional[List['PostInDb']]
    followers:Optional[List['User']]
    following:Optional[List['User']]
    messages:Optional[List['MessageInDb']]
    chats:Optional[List['ChatInDb']]


