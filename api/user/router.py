from typing import Annotated
from user.schema import User, UserInDb, UserShow, UserUpdate
from response_generic import IResponseBase
from fastapi import Depends,APIRouter, Form
from .service_template import UserServiceTemplate
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import get_current_active_user,get_db

router = APIRouter()

@router.post("/account",tags=['show'])
async def show_account(db:AsyncSession = Depends(get_db),current_user = Depends(get_current_active_user)):
    user_account = await UserServiceTemplate().get_me(current_user,db)
    return (IResponseBase[UserShow](data=user_account,status="success"))

@router.post("/create_account",tags = ["show"])
async def create_account(username = Form(),email = Form(),password = Form(),db:AsyncSession = Depends(get_db)):
    user = await UserServiceTemplate().create_account(username,email,password,db)
    return (IResponseBase[User](data=user,status="success"))

@router.post("/account/{username}",tags = ["show"])
async def get_user_accont(username:str,db = Depends(get_db)):
    user_account = await UserServiceTemplate().get_user_account(username,db)
    return (IResponseBase[UserShow](status="success",data=user_account))

@router.post("/follow",tags=['user'])
async def follow(username:str = Form(),current_user = Depends(get_current_active_user),db:AsyncSession = Depends(get_db)):
    result = await UserServiceTemplate().follow(username,current_user,db)
    return (IResponseBase(status=result))

@router.post("/unfollow",tags = ['user'])
async def unfollow(username:str = Form(),current_user = Depends(get_current_active_user),db:AsyncSession = Depends(get_db)):
    result = await UserServiceTemplate().unfollow(username,current_user,db)
    return (IResponseBase(status=result))

@router.delete("/delete",tags=["user"])
async def delete_user(current_user:Annotated[UserInDb,Depends(get_current_active_user)],db:AsyncSession = Depends(get_db)):
    result =  await UserServiceTemplate().delete_user(db,current_user.id)
    return (IResponseBase(status=result))

@router.put("/update",response_model=UserUpdate,tags=["user"])
async def updtade_uer(user:UserUpdate,currcurrent_user:Annotated[UserInDb,Depends(get_current_active_user)],db:AsyncSession = Depends(get_db)):
    user =  await UserServiceTemplate().update_user(db,user,currcurrent_user.id)
    return (IResponseBase[User](data=user,status="success"))