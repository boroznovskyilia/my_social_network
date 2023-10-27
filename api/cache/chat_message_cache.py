import json
from fastapi.encoders import jsonable_encoder
from template_routers.schema import ShowChat,Message
from chat.service import ChatService
from .base_cache import Cache
from sqlalchemy.ext.asyncio import AsyncSession
from redis import asyncio as aioredis

class ChatMessageCache(Cache):

    async def get_from_cache(self,chat_id):
        cached_messages = await self.redis.get(f"chat_messages_{chat_id}")
        if cached_messages:
            cached_messages = json.loads(cached_messages)
            cached_messages = ShowChat(
                previous_messages=cached_messages
            )
            return cached_messages
        return None
    
    async def refresh_cache(self,chat,db:AsyncSession,current_user):
        previous_messages = await ChatService().prev_messages(chat.id,db,current_user)
        res_chat =  ShowChat(
            previous_messages=previous_messages
        )
        previous_mess = jsonable_encoder(previous_messages)
        await self.redis.set(f"chat_messages_{chat.id}",json.dumps(previous_mess))
        return res_chat
    
    async def del_cache(self,chat_id):
        await self.redis.delete(f"chat_messages_{chat_id}")

    async def add_message_to_cache(self,chat_id,message):
        # cached_messages = await self.redis.get(f"chat_messages_{chat_id}")
        # if cached_messages:
        #     cached_messages = json.loads(cached_messages)
        #     cached_messages = ShowChat(
        #         previous_messages=cached_messages
        #     )
        username,text = message.split(': ',1)
        message_data = Message(
            username=username,
            text = text
        )
        # cached_messages.previous_messages.append(message_data)
        # cached_messages = jsonable_encoder(cached_messages.previous_messages)
        message_data = jsonable_encoder(message_data)
        messages = json.dumps(message_data)
        await self.redis.rpush(f"chat_messages_{chat_id}",messages)

class RedisPubSubManager:
    def __init__(self, host='localhost', port=6379):
        self.redis_host = host
        self.redis_port = port
        self.pubsub = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        return aioredis.Redis(host=self.redis_host,
                              port=self.redis_port,
                              auto_close_connection_pool=False)

    async def connect(self) -> None:
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def _publish(self, chat_id: str, message: str) -> None:
        await self.redis_connection.publish(chat_id, message)

    async def subscribe(self, chat_id: str) -> aioredis.Redis:
        await self.pubsub.subscribe(chat_id)
        return self.pubsub

    async def unsubscribe(self, chat_id: str) -> None:
        await self.pubsub.unsubscribe(chat_id)