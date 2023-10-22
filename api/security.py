from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt  
from datetime import datetime, timedelta
from typing import Union
from config import SECRET_KEY,ALGORITHM
import secrets

ACCESS_TOKEN_EXPIRE_MINUTES = 15

token = jwt.encode({'key': 'value'}, 'secret', algorithm = ALGORITHM)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer("/login")

def verify_password(given_password, hashed_password):
    return pwd_context.verify(given_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_access_token(data: dict,expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt