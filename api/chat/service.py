from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import Chat as chat_table
from db.models.models import Message as message_table
from db.models.models import association_chat_table
from sqlalchemy import select,delete
from sqlalchemy.orm import selectinload
from .schema import Message


class ChatService():

    async def get_chat_ojb(self,chat_id:int,db:AsyncSession,):
        query = select(chat_table).where(chat_table.id == chat_id).\
        options(selectinload(chat_table.users),
                selectinload(chat_table.messages))
        res = await db.execute(query)
        return res.scalars().first()
    
    async def get_chat(self,db:AsyncSession,chat_id):
        query = select(chat_table).where(chat_table.id == chat_id)
        res = await db.execute(query)
        return res.scalars().first()
    
    async def get_chat_by_name(self,db:AsyncSession,chat_name):
        query = select(chat_table).where(chat_table.name == chat_name)
        res = await db.execute(query)
        return res.scalars().all()
    
    async def get_chats_for_user(self,db:AsyncSession,user_id):
        query = select(chat_table).join(association_chat_table,chat_table.id == association_chat_table.c.chat_id).\
        options(selectinload(chat_table.users)).\
        filter(association_chat_table.c.user_id== user_id).order_by()
        posts = await db.execute(query)
        return posts.scalars().all()
    
    async def create_chat(self,db:AsyncSession,username):
        chat = chat_table(
            name = username
        )
        db.add(chat)
        await db.commit()
        await db.refresh(chat)
        return chat
    
    async def add_user_to_chat(self,db:AsyncSession,chat,user):
        chat.users.append(user)
        await db.commit()
        return chat

    async def remove_user_from_chat(self,db:AsyncSession,chat,user):
        chat.users.remove(user)
        await db.commit()
        return chat
    
    async def delete_chat(db:AsyncSession,chat_id):
        query = delete(chat_table).where(chat_table.id == chat_id)
        await db.execute(query)
        await db.commit()

    async def prev_messages(self,chat_id:int,db:AsyncSession,current_user):
        get_chat = await self.get_chat(db,chat_id)
        if get_chat is None:
            raise HTTPException(400,"chat not found")
        messages = await MessageService().get_chat_messages(db,chat_id)
        messages_show = []
        for message in messages:
            buffer = Message(
                username=message.user.username,
                text = message.text
            )
            messages_show.append(buffer)
        return (messages_show)


class MessageService():
    async def add_message(self,db:AsyncSession,chat_id:int,mes_text:str,user_id:int):
        message = message_table(
            text = mes_text,
            chat_id = chat_id,
            user_id = user_id,
        )
        db.add(message)
        await db.commit()
        return message
    
    async def delete_message(self,db:AsyncSession,message_id):
        query = delete(message_table).where(message_table.id == message_id)
        await db.execute(query)
        await db.commit()

    async def get_chat_messages(self,db:AsyncSession,chat_id:int):
        query = select(message_table).where(message_table.chat_id == chat_id).\
        options(selectinload(message_table.user)).order_by(message_table.send_time)
        posts = await db.execute(query)
        return posts.scalars().all()
    