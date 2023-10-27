from pydantic import BaseModel
from chat.schema import ChatInChats,Message
from typing import List

class PostCreate(BaseModel):
    article:str
    content:str     
   
class PostShow(PostCreate):
    id:int
    user_id:int

class ShowChat(BaseModel):
    # user_id:int
    # chat:ChatInChats
    # user_name:str
    previous_messages:List[Message]

class ShowUsers(BaseModel):
    users:List[str]
