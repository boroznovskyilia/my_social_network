from fastapi import Depends,APIRouter
from user.schema import UserInDb
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import get_db,get_current_active_user
from .service import AuthService
from template_routers.router import router


@router.post("/login",tags=["auth"])
async def login(*,db: AsyncSession = Depends(get_db),form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    return(await AuthService.login(db,form_data))

@router.post("/logout",tags=["auth"])
async def logout(current_user: Annotated[UserInDb, Depends(get_current_active_user)]):
    return{f"{current_user.username} was logged out"}




    
   


