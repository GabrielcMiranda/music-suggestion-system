from datetime import datetime, timedelta
from app.core.database.connection import async_session
from app.schemas import LoginRequest, Token
from sqlalchemy.future import select
from sqlalchemy import or_
from app.models import User
from app.core.security import bcrypt_context
from app.core.settings import Settings
from fastapi import HTTPException
from jose import jwt, JWTError
class AuthService:

    async def login(dto:LoginRequest):
        async with async_session() as session:
            result = await session.execute(select(User).where(or_(User.username == dto.login, User.username == dto.login)))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=404,detail='invalid user or password')
            elif not bcrypt_context.verify(dto.password, user.password):
                raise HTTPException(status_code=404,detail='invalid password')
            
            encode = {'subject':user.id}
            expires = datetime.utcnow()+ timedelta.seconds(36000)
            encode.update({'exp':expires})
            token = jwt.encode(encode, Settings.SECRET_KEY, Settings.ALGORITHM)

            return Token(access_token=token, token_type='bearer')
            

