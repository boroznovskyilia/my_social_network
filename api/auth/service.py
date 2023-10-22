from datetime import timedelta
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from user.service_db import UserServiceDB as User
from fastapi.responses import JSONResponse
from response_generic import IResponseBase
from .schema import Token,Erorr
from fastapi.encoders import jsonable_encoder

class AuthService():
    async def login(db: AsyncSession,form_data):
        user = await User().authenticate_user(db,form_data.username,form_data.password)
        if not user:
           response_data = IResponseBase[Erorr](status="error",data=Erorr(detail="Wrong username or password"))
           return JSONResponse(content=jsonable_encoder(response_data),status_code=400)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        response_data = IResponseBase[Token](status="success",data=Token(
            access_token=access_token,
            token_type="bearer"
        ))
        # return JSONResponse(content=jsonable_encoder(response_data),status_code=200)
        return {"access_token": access_token, "token_type": "bearer"}
