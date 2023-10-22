import json
from fastapi.encoders import jsonable_encoder
from user.schema import UserShow
from user.service_db import UserServiceDB
from .base_cache import Cache
from sqlalchemy.ext.asyncio import AsyncSession

class AccountCache(Cache):

    async def get_from_cache(self,user_id):
        cached_posts = await self.redis.get(f"user_account_{user_id}")
        if cached_posts:
            return json.loads(cached_posts)
        return None

    async def refresh_cache(self,user_id,db:AsyncSession):
        user_account = await UserServiceDB().get_user_account(user_id,db)
        account=UserShow(
            username=user_account.username,
            email=user_account.email,
            date_create = user_account.date_create,
            followers=user_account.followers,
            following=user_account.following,
            posts=user_account.posts
        )
        data = jsonable_encoder(account)
        await self.redis.set(name = f"user_account_{user_id}",value = json.dumps(data),ex=10)
        return account

