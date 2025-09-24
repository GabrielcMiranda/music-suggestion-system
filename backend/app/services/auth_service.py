from datetime import datetime, timedelta
from app.core.database.connection import async_session
from app.schemas import LoginRequest, Token, RegisterRequest
from sqlalchemy.future import select
from sqlalchemy import or_
from app.models import User
from app.core.security import bcrypt_context, oauth2_bearer
from app.core.settings import Settings
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
class AuthService:

    async def login(self, dto:LoginRequest):
        async with async_session() as session:

            result = await session.execute(select(User).where(or_(User.username == dto.login, User.email == dto.login)))
            user = result.scalar_one_or_none()

            if not user or not bcrypt_context.verify(dto.password, user.password):
                raise HTTPException(status_code=404,detail='invalid credentials.')
            
            return self.build_JWT(str(user.id))


    async def register(dto:RegisterRequest):
        async with async_session() as session:

            result = await session.execute(select(User).where(or_(User.username == dto.username, User.email == dto.email)))
            user = result.scalars().all()

            if user:
                raise HTTPException(status_code=409,detail='username or email are already been used')
            
            user = User(username = dto.username, email = dto.email, password = bcrypt_context.hash(dto.password))
            session.add(user)

            await session.commit()


    def validate_user_auth(token:str = Depends(oauth2_bearer)):
        try:

            payload = jwt.decode(token=token, key= Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
            user_id = payload.get('subject')

            if not user_id:
                raise HTTPException(401, 'invalid token')
            
            return user_id
        
        except JWTError:
            raise HTTPException(401, 'invalid token')
     
        
    def build_JWT(user_id:str):

        encode = {'subject':user_id}
        expires = datetime.utcnow()+ timedelta(minutes= int(Settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        encode.update({'exp':expires})
        token = jwt.encode(encode, Settings.SECRET_KEY, Settings.ALGORITHM)

        return Token(access_token=token, token_type='bearer')