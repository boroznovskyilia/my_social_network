from pydantic import BaseModel,Field
import datetime

class PostCreate(BaseModel):
    article:str = Field(max_length=100)
    content:str = Field(max_length = 1000)
    class Config:
        from_attributes = True

class MyPost(PostCreate):
    id:int
    date_create:datetime.datetime

class PostShow(PostCreate):
    date_create:datetime.datetime
    username:str
    
    
class PostInDb(PostCreate):
    id: int  = Field(ge = 1)
    user_id:int = Field(ge=1)
    date_create:datetime.datetime
    username:str

