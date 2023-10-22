from sqlalchemy import select,delete,update
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import User as user_table
from db.models.models import Post as post_table
from db.models.models import association_table
from posts.schema import PostCreate
from sqlalchemy.orm import selectinload

class PostsServiceDB():
    
    async def create_post(self,user_id:int,user_name:str,post:PostCreate,db:AsyncSession):
        post = post_table(
            article=post.article,
            content=post.content,
            user_id=user_id,
            username = user_name,
        )
        db.add(post)
        await db.commit()
        return post
    
    async def delete_post(self,id,db:AsyncSession):
        query = delete(post_table).where(post_table.id == id)
        await db.execute(query)

    async def get_post(self,id,db:AsyncSession):
        query = select(post_table).where(post_table.id == id)
        res = await db.scalar(query)
        return res  

    async def get_posts_for_user(self,db:AsyncSession,user_id):
        query = select(post_table).join(association_table,post_table.user_id == association_table.c.followed_id).\
        options(selectinload(post_table.user)).\
        filter(association_table.c. follower_id== user_id).order_by(post_table.date_create.desc())
        posts = await db.execute(query)
        return posts.scalars().all()
    
    async def update_post(self,db:AsyncSession,post_id,post:PostCreate):
        query = update(post_table).where(post_table.id == post_id).values(article = post.article,content = post.content)
        await db.execute(query)
        await db.commit()
        return post
    
    async def delete_post(self,db:AsyncSession,post_id):
        query = delete(post_table).where(post_table.id == post_id)
        await db.execute(query)
        await db.commit()
        

        
        