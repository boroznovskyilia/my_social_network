from typing import AsyncGenerator
from db.database import async_session_maker
from fastapi import Depends, HTTPException,status
from jose import JWTError,jwt
from sqlalchemy.ext.asyncio import AsyncSession
from config import SECRET_KEY
from security import oauth2_scheme,ALGORITHM
from user.schema import UserInDb
from auth.schema import TokenData
from user.service_db import UserServiceDB as User
from typing_extensions import Annotated
from response_generic import IResponseBase

async def get_db() -> AsyncGenerator:
    try:
        db = async_session_maker()
        yield db
    finally:
        await db.close()

async def get_current_user(*,db:AsyncSession = Depends(get_db),token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization":"Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            IResponseBase[str](status="unsuccess")
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    id = int(id)
    user = await User().get_user(id=int(token_data.id),db=db)
    if user is None:
        IResponseBase[str](status="unsuccess")
        raise credentials_exception
    return user


async def get_current_active_user(*,current_user: Annotated[UserInDb,Depends(get_current_user)]):
    return current_user
