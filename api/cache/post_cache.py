import json
from fastapi.encoders import jsonable_encoder
from posts.service_db import PostsServiceDB
from posts.schema import PostShow
from .base_cache import Cache
from sqlalchemy.ext.asyncio import AsyncSession

class PostCache(Cache):

    async def get_from_cache(self,user_id):
        cached_posts = await self.redis.get(f"user_posts_{user_id}")
        if cached_posts:
            return json.loads(cached_posts)
        return None

    async def refresh_cache(self,user_id,db:AsyncSession):
        user_posts_obj = await PostsServiceDB().get_posts_for_user(db,user_id)
        user_posts = []
        for post in user_posts_obj:
            buf_post = PostShow(
                article=post.article,
                content=post.content,
                date_create=post.date_create,
                username=post.user.username
                )
            user_posts.append(buf_post)
        users = jsonable_encoder(user_posts)
        await self.redis.set(name = f"user_posts_{user_id}",value = json.dumps(users),ex=10)
        return user_posts

