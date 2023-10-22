from sqlalchemy import select,update,delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import User as user_table
from user.schema import UserCreate,UserUpdate
from security import get_password_hash
from security import verify_password
from sqlalchemy.orm import selectinload
from security import get_password_hash

class UserServiceDB():
    
    async def get_user(self,id,db:AsyncSession):
        query = select(user_table).where(user_table.id == id)
        result = await db.scalar(query)
        return result
    
    async def get_user_account(self,id,db:AsyncSession):
        query = (
            select(user_table)
            .where(user_table.id == id)
            .options(
                selectinload(user_table.followers),
                selectinload(user_table.following),
                selectinload(user_table.posts),
                selectinload(user_table.chats),
                selectinload(user_table.messages),  
            )
        )

        result = await db.execute(query)
        user = result.scalars().first()
        return user

    
    async def get_user_by_name(self,username,db:AsyncSession):
        query = select(user_table).where(user_table.username == username)
        result = await db.scalar(query)
        return result

    async def create_user(self,user:UserCreate,db:AsyncSession):
        hashed = get_password_hash(user.password)
        user = user_table(
            username=user.username,
            email=user.email,
            hashed_password = hashed
        )
        db.add(user)
        await db.commit()
        return user
    
    async def update_user(self,id,user:UserUpdate,db:AsyncSession):
        h_password = get_password_hash(user.password)
        query = update(user_table).where(user_table.id == id).values(username = user.username,email = user.email,hashed_password = h_password)
        res = await db.scalar(query)
        return res

    async def delete_user(self,id,db:AsyncSession):
        query = delete(user_table).where(user_table.id == id)
        await db.execute(query)
    
    async def authenticate_user(self,db:AsyncSession,username: str, password: str):
        get_user = await self.get_user_by_name(username,db)
        if not get_user:
            return False
        
        hashed_password = get_user.hashed_password
        if not verify_password(password, hashed_password):
            return False
        return get_user

    async def subscribe(self,db:AsyncSession,user,follow_user):
        user.following.append(follow_user)
        await db.commit()
        return user
    
    async def unsubscribe(self,db:AsyncSession,user,follow_user):
        user.following.remove(follow_user)
        await db.commit()
        return user

    async def delete_user(self,db:AsyncSession,user_id):
        query = delete(user_table).where(user_table.id == user_id)
        await db.execute(query)
        await db.commit()
        return {"status":"success"}
    
    async def update_user(self,db:AsyncSession,user:UserUpdate,user_id):
        hash_password = get_password_hash(user.password)
        query = update(user_table).where(user_table.id == user_id).\
            values(username = user.username,email=user.email,hashed_password = hash_password)
        await db.execute(query)
        await db.commit()
        

