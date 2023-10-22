from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Form,APIRouter
from auth.utils import get_current_active_user, get_db
from .service_template import PostServiceTemplate
from response_generic import IResponseBase
from typing import List
from .schema import PostShow,PostCreate

router = APIRouter()

@router.post("/posts",tags=["posts"])
async def show_posts(db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
    user_posts = await PostServiceTemplate().show_post_for_user(db,current_user)
    return (IResponseBase[List[PostShow]](data=user_posts,status="success"))

@router.post("/create_post",tags=['posts'])
async def create_post(article = Form(),content = Form(),current_user = Depends(get_current_active_user),db = Depends(get_db)):
    post = await PostServiceTemplate().create_post(article,content,current_user,db)
    return (IResponseBase[PostShow](data=post,status="success"))
