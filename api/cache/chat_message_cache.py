import json
from fastapi.encoders import jsonable_encoder
from template_routers.schema import ShowChat
from chat.service import ChatService
from .base_cache import Cache
from sqlalchemy.ext.asyncio import AsyncSession

class ChatMessageCache(Cache):

    async def get_from_cache(self,chat_id):
        cached_messages = await self.redis.get(f"chat_messages_{chat_id}")
        if cached_messages:
            return json.loads(cached_messages)
        return None

    async def refresh_cache(self,chat,db:AsyncSession,current_user):
        previous_messages = await ChatService().prev_messages(chat.id,db,current_user)
        res_chat =  ShowChat(
            chat = chat,
            user_id =current_user.id,
            user_name=current_user.username,
            previous_messages=previous_messages
        )
        users = jsonable_encoder(chat)
        await self.redis.set(name = f"chat_messages_{chat.id}",value = json.dumps(users),ex=1)
        return res_chat

