from fastapi import APIRouter,Depends,HTTPException,status
from auth.utils import get_db,get_current_active_user
from user.schema import UserCreate,UserInDb,UserUpdate,User,UserShow
from sqlalchemy.ext.asyncio import AsyncSession
from user.service_db import UserServiceDB
from typing import Annotated
from cache.account_cache import AccountCache

class UserServiceTemplate(UserServiceDB):
    
    async def get_me(self,current_user,db:AsyncSession):
        current_user_id = current_user.id
        user = await super().get_user_account(current_user_id,db)
        user = UserShow(username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                date_create=user.date_create,
                followers=user.followers,
                following=user.following,
                posts=user.posts
                )
        return user
    
    async def get_user_account(self,username:str,db):
        get_user = await super().get_user_by_name(username,db)
        cached_account = await AccountCache().get_from_cache(get_user.id)
        if cached_account:
            user_account = cached_account
        else:
            user_account = await AccountCache().refresh_cache(get_user.id,db)
        return user_account
    
    async def create_account(self,username,email,password,db):
        user_data = UserCreate(
        username=username,
        email=email,
        password=password
        )
        db_user = await super().get_user_by_name(user_data.username,db)
        if db_user:
            raise HTTPException(status_code=400, detail="This username has been already registered")
        user = await super().create_user(user_data,db)
        return user
    
    async def follow(self,username:str,current_user,db:AsyncSession):
        follow_user = await super().get_user_by_name(username,db)
        if follow_user is None:     
            raise HTTPException(status_code=401,detail = "User to follow doesn't exist")
        current_user_account = await super().get_user_account(current_user.id,db)
        follow_user_account = await super().get_user_account(follow_user.id,db)
        if follow_user_account in current_user_account.following:
            raise HTTPException(status_code=401,detail = "You have already followed by this user")
        await super().subscribe(db,current_user_account,follow_user_account)
        return ("success")
        
    async def unfollow(self,username:str,current_user ,db:AsyncSession):
        follow_user = await super().get_user_by_name(username,db)
        if follow_user is None:     
            raise HTTPException(status_code=401,detail = "User to follow doesn't exist")
        current_user_account = await super().get_user_account(current_user.id,db)
        follow_user_account = await super().get_user_account(follow_user.id,db)
        if follow_user_account not in current_user_account.following:
            raise HTTPException(status_code=401,detail = "You don't follow this user")
        await super().unsubscribe(db,current_user_account,follow_user_account)
        return ("success")
    
    async def delete_user(current_user,db:AsyncSession = Depends(get_db)):
        await super().delete_user(db,current_user.id)
        return 
    
    async def update_user(user:UserUpdate,user_id,db:AsyncSession):
        is_user = await super().get_user_by_name(user.username,db)
        if is_user:
            raise HTTPException(status_code=400,detail="User with this username already exists")
        else:
            await super().update_user(db,user,user_id)
            return user


    






