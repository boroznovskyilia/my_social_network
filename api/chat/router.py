from typing import List
from fastapi import APIRouter, Depends, Form, WebSocket
from template_routers.schema import ShowChat, ShowUsers
from user.schema import UserShow
from auth.utils import get_current_active_user, get_db
from chat.schema import ChatInChats
from response_generic import IResponseBase
from sqlalchemy.ext.asyncio import AsyncSession
from .service_template import ChatSeviceTemplate
from .service import ChatService

router = APIRouter()


@router.post("/chats",tags = ["chat"])
async def show_chats(db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
    chats = await ChatSeviceTemplate().get_chats_for_user(db,current_user)
    return (IResponseBase[List[ChatInChats]](data=chats,status="success"))

@router.post("/chats/create",tags = ['chat'])
async def create_chat(name:str = Form(),db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
    await ChatSeviceTemplate().create_chat(name,db,current_user)
    return (IResponseBase[UserShow](status="success"))

@router.post("/chats/{chat_id}",tags=["chat"])
async def show_chat(chat_id:int,current_user = Depends(get_current_active_user),db = Depends(get_db)):
    chat = await ChatSeviceTemplate().show_chat(chat_id,current_user,db)
    return (IResponseBase[ShowChat](status="success",data = chat))

@router.websocket("/chats/{chat_id}")
async def show_chat(websocket:WebSocket,chat_id:int,db = Depends(get_db)):
    await ChatSeviceTemplate().connect_chat(websocket,chat_id,db)

@router.post("/chats/{chat_id}/add_user",tags = ["chat"])
async def add_user(chat_id:int,name:str = Form(),db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
    result = await ChatSeviceTemplate().add_user(chat_id,name,db,current_user)
    return result

@router.delete("/chats/{chat_id}/leave",tags = ["chat"])
async def leave(chat_id:int,db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
    result = await ChatSeviceTemplate().leave_chat(chat_id,db,current_user)
    return (IResponseBase(status=result))

@router.post("/chats/{chat_id}/members",tags = ["chat"])
async def members(chat_id:int,db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
    users = await ChatSeviceTemplate().get_members_of_chat(chat_id,db)
    return (IResponseBase[ShowUsers](status="success",data=ShowUsers(users=users)))