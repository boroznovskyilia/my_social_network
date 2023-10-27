from fastapi import WebSocket
from typing import List
from cache.chat_message_cache import RedisPubSubManager,ChatMessageCache
import asyncio
from redis import asyncio as aioredis

class WebSocketManager:
    def __init__(self):
        self.chats: dict = {}
        self.pubsub_client = RedisPubSubManager()

    async def add_user(self, chat_id: str, websocket: WebSocket) -> None:
        await websocket.accept()

        if chat_id in self.chats:
            self.chats[chat_id].append(websocket)
        else:
            self.chats[chat_id] = [websocket]

            await self.pubsub_client.connect()
            pubsub_subscriber = await self.pubsub_client.subscribe(chat_id)
            asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))

    async def broadcast(self, chat_id: str, message: str) -> None:
       await self.pubsub_client._publish(chat_id, message)

    async def remove_user(self, chat_id: str, websocket: WebSocket) -> None:
        self.chats[chat_id].remove(websocket)

        if len(self.chats[chat_id]) == 0:
            del self.chats[chat_id]
            await ChatMessageCache().del_cache(chat_id)
            await self.pubsub_client.unsubscribe(chat_id)
            
    async def _pubsub_data_reader(self, pubsub_subscriber:aioredis.Redis):
        while True:
            message = await pubsub_subscriber.get_message(ignore_subscribe_messages=True)
            if message is not None:
                chat_id = int(message['channel'].decode('utf-8'))
                all_sockets = self.chats[chat_id]
                for socket in all_sockets:
                    data = message['data'].decode('utf-8')
                    await socket.send_text(data)