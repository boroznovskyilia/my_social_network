from typing import Any, Optional
from sqlalchemy import Integer,String,Boolean,MetaData,DateTime,Table,Column,ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy.sql import func
import datetime
from typing import List

class Base(DeclarativeBase):
    pass

association_table = Table("association_table",
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id',ondelete="CASCADE"),primary_key=True),
    Column('followed_id', Integer, ForeignKey('user.id',ondelete="CASCADE"), primary_key=True)
    )


association_chat_table = Table(
    "association_chat_table",
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat.id',ondelete="CASCADE"),primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id',ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    id:Mapped[Optional[int]] = mapped_column(Integer,primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String,nullable=False)
    hashed_password:Mapped[Optional[str]] = mapped_column(String,nullable=False)
    email:Mapped[Optional[str]] = mapped_column(String,nullable=False)
    date_create:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    messages:Mapped[Optional[List["Message"]]] = relationship(back_populates="user",cascade="all, delete")

    chats:Mapped[Optional[List["Chat"]]] = relationship(
        secondary=association_chat_table,\
        cascade="all, delete",back_populates='users'
    )

    posts:Mapped[Optional[List["Post"]] ]= relationship(back_populates="user",cascade="all, delete")

    followers:Mapped[Optional[List["User"]]] = relationship('User',\
        secondary=association_table,\
        primaryjoin=id==association_table.c.followed_id,\
        secondaryjoin=id == association_table.c.follower_id,\
        cascade="all, delete",back_populates='following')
    
    following:Mapped[Optional[List["User"]]] = relationship('User',\
        secondary=association_table,\
        primaryjoin=id == association_table.c.follower_id,\
        secondaryjoin=id == association_table.c.followed_id,\
        cascade="all, delete",back_populates='followers')

    def __init__(self, username,email,hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

class Post(Base):
    __tablename__ = "post"
    id:Mapped[Optional[int]] = mapped_column(Integer,primary_key=True)
    article:Mapped[Optional[String]] = mapped_column(String,nullable=False)
    content:Mapped[Optional[String]] = mapped_column(String,nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id",ondelete="CASCADE"))
    user:Mapped[Optional["User"]] = relationship(back_populates="posts")
    date_create:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    

    def __init__(self, article,content,user_id,username):
        self.article = article
        self.content = content
        self.user_id = user_id
        self.username = username


class Chat(Base):
    __tablename__ = "chat"

    id:Mapped[Optional[int]] = mapped_column(Integer,primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String,nullable=False)
    users:Mapped[Optional[List["User"]]] = relationship(
        secondary=association_chat_table,\
        cascade="all, delete",back_populates='chats'
    )
    messages:Mapped[Optional[List["Message"]]] = relationship(back_populates="chat",cascade="all, delete")
    

class Message(Base):
    __tablename__ = "message"
    id:Mapped[Optional[int]] = mapped_column(Integer,primary_key=True)
    chat_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chat.id",ondelete="CASCADE"))
    chat:Mapped[Optional["Chat"]] = relationship(back_populates="messages")
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id",ondelete="CASCADE"))
    user:Mapped[Optional["User"]] = relationship(back_populates="messages")
    send_time:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    text:Mapped[Optional[String]] = mapped_column(String,nullable=False)
    def __init__(self,text,chat_id,user_id):
        self.text = text
        self.chat_id = chat_id
        self.user_id = user_id