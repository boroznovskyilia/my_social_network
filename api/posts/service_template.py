from fastapi import APIRouter,Depends,HTTPException,status
from auth.utils import get_db,get_current_active_user
from posts.schema import PostCreate,PostShow
from sqlalchemy.ext.asyncio import AsyncSession
from posts.service_db import PostsServiceDB
from typing import List
from cache.post_cache import PostCache
import json


class PostServiceTemplate(PostsServiceDB):

    async def create_post(self,article,content,current_user,db:AsyncSession):
        post_data = PostCreate(
        article = article,
        content = content,
        )
        post = await super().create_post(current_user.id,current_user.username,post_data,db)
        return post


    async def show_post_for_user(self,db:AsyncSession,current_user):
        cached_posts = await PostCache().get_from_cache(current_user.id)
        if cached_posts:
            user_posts = cached_posts
        else:
            posts = await PostCache().refresh_cache(current_user.id,db)
            user_posts = posts

        return user_posts

    async def update_post(self,post_id:int,post:PostCreate,db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
        updating_post = await super().get_post(post_id,db)
        if updating_post:
            post = await super().update_post(db,post_id,post)
            return post
        else:
            raise HTTPException(401,detail="There is no this post")
        

    async def delete_post(self,post_id:int,db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
        deleting_post = await super().get_post(post_id,db)
        if deleting_post:
            await super().delete_post(db,post_id)
            return {"status":"success"}
        else:
            raise HTTPException(401,detail="There is no this post")