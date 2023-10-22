from redis import asyncio as aioredis   
import json
from posts.schema import PostShow
from posts.service_db import PostsServiceDB
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from abc import ABC,abstractmethod

class Cache(ABC):
    def __init__(self):
        self.redis = aioredis.from_url("redis://127.0.0.1:6379",decode_responses = True)

    @abstractmethod
    async def get_from_cache(self,user_id):
        pass
    @abstractmethod
    async def refresh_cache(self,user_id,db:AsyncSession):
        pass
