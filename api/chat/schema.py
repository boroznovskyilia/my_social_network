from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    username:str
    text:str

class ChatCreate(BaseModel):
    name:str
    class Config:
        from_attributes = True

class ChatShow(ChatCreate):
    messages:List["Message"]


class ChatInDb(BaseModel):
    id:int

class MessageInDb(Message):
    id:int
    user_id:int
    chat_id:int
    text:str

class ChatInChats(BaseModel):
    id:int
    name:str
    class Config:
        from_attributes = True
