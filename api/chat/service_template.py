from fastapi import APIRouter, Depends,HTTPException, WebSocket, WebSocketDisconnect
from user.service_db import UserServiceDB
from sqlalchemy.ext.asyncio import AsyncSession
from chat.service import ChatService,MessageService
from chat.schema import ChatInChats
from .ws import WebSocketManager as ws_manager
from cache.chat_message_cache import ChatMessageCache
from auth.utils import get_current_active_user,get_user_by_token_from_ws
from starlette.websockets import WebSocket as StarletteWebsocket

router = APIRouter()

class ChatSeviceTemplate(ChatService):
    async def create_chat(self,name:str,db:AsyncSession,current_user):
        chat = await super().create_chat(db,name)
        chat_obj = await super().get_chat_ojb(chat.id,db)
        user_account = await UserServiceDB().get_user_account(current_user.id,db)
        chat = await super().add_user_to_chat(db,chat_obj,user_account)
    
    async def get_chats_for_user(self,db:AsyncSession,current_user):
        user_id = current_user.id
        chats = await super().get_chats_for_user(db,user_id)
        user_chats = []
        for chat in chats:
            buf_chat = ChatInChats(
                id = chat.id,
                name = chat.name)
            user_chats.append(buf_chat)
        return user_chats

    
    async def show_chat(self,chat_id:int,current_user,db:AsyncSession):
        chat = await super().get_chat_ojb(chat_id,db)
        if current_user in chat.users:
            cached_messages = await ChatMessageCache().get_from_cache(chat_id)
            if cached_messages:
                return cached_messages
            else:
                previous_messages = await ChatMessageCache().refresh_cache(chat,db,current_user)
                return previous_messages
        else:
            raise HTTPException(400,"you are not a memeber of this chat")

    async def connect_chat(self,websocket:WebSocket,chat_id:int,db):
        manager = ws_manager()
        await manager.add_user(chat_id,websocket)
        try:
            while True:
                data = await websocket.receive_json()
                text = data.get('text')
                token = data.get('token')
                current_user = await get_user_by_token_from_ws(token,db)
                # user_name = current_user.username
                # user_id = current_user.id
                # await manager.send_personal_message(f"You: {text}", websocket)
                await manager.broadcast(chat_id,f"{current_user.username}: {text}")
                await ChatMessageCache().add_message_to_cache(chat_id,f"{current_user.username}: {text}")
                await MessageService().add_message(db,chat_id,text,current_user.id)
        except WebSocketDisconnect:
            await manager.remove_user(chat_id,websocket)
            
    
    async def add_user(self,chat_id:int,name:str,db,current_user):
        get_chat = await super().get_chat_ojb(chat_id,db)
        if get_chat is None:
            raise HTTPException(400,"chat not found")
        if current_user in get_chat.users:
            get_user = await UserServiceDB().get_user_by_name(name,db)
            if not get_user:
                raise HTTPException(status_code=400,detail = "This user doesn't exist")
            else:
                get_chat_user = await UserServiceDB().get_user_account(get_user.id,db)
                await super().add_user_to_chat(db,get_chat,get_chat_user)
                return {"status":"success"}
        else:
            raise HTTPException(400,"you are not a memeber of this chat")
        
    async def leave_chat(self,chat_id:int,db:AsyncSession,current_user):
        get_chat = await super().get_chat_ojb(chat_id,db)
        if get_chat is None:
            raise HTTPException(400,"chat not found")
        if current_user in get_chat.users:
            get_user = await UserServiceDB().get_user_by_name(current_user.username,db)
            if not get_user:
                raise HTTPException(status_code=400,detail = "This user doesn't exist")
            else:
                get_chat_user = await UserServiceDB().get_user_account(get_user.id,db)
                await super().remove_user_from_chat(db,get_chat,get_chat_user)
                members = await self.get_members_of_chat(chat_id,db)
                if len(members) == 0:
                    await super().delete_chat(db,chat_id)
                return ("success")
        else:
            raise HTTPException(400,"you are not a memeber of this chat")

    async def get_members_of_chat(self,chat_id:int,db:AsyncSession):
        chat = await super().get_chat_ojb(chat_id,db)
        users = []
        for user in chat.users:
            users.append(user.username)
        return users
    