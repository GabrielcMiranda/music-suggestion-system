from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import update
from app.models import User
from app.schemas import ProfileResponse, OtherProfileResponse
from app.core.database.connection import async_session
from uuid import UUID
import logging

class UserService:


    async def get_profile(username:str , user_id: UUID):
        async with async_session() as session:

            username_query = await session.execute(select(User).where(User.username == username))
            username_result = username_query.scalar_one_or_none()

            user_id_query = await session.execute(select(User).where(User.id == user_id))

            user_id_result = user_id_query.scalar_one_or_none()
            if not user_id_result:
                raise HTTPException(status_code=401, detail='Invalid credentials')

            elif not username_result:
                raise HTTPException(status_code=404, detail='User not found')
            
            if username_result == user_id_result:
                user = user_id_result
                logging.info('usuarios iguais')

                if not user.favorite_music_genre:
                    music_genre = 'You gotta generate at least one recommendation to verify your verify your favorite music genre'

                return ProfileResponse(username=user.username, email=user.email, favorite_music_genre=music_genre, profile_picture=user.profile_picture)
            
            else:
                user = username_result

                if not user.favorite_music_genre:
                    music_genre = 'This user has not generated any recommendations yet'
                
                return OtherProfileResponse(username=user.username, favorite_music_genre=music_genre, profile_picture=user.profile_picture)

    async def update_profile_picture(user_id:UUID, profile_picture_url:str):
        async with async_session() as session:

            result = await session.execute(update(User).where(User.id == user_id).values(profile_picture=profile_picture_url).returning(User.id))
            user = result.scalar_one_or_none()
            await session.commit()
            
            if not user:
                raise HTTPException(status_code=404, detail='User not found')
            
            
        
