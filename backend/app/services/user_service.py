from fastapi import HTTPException
from sqlalchemy.future import select
from app.models import User
from app.schemas import ProfileResponse
from app.core.database.connection import async_session
from uuid import UUID

class UserService:


    async def get_profile(user_id: UUID):
        async with async_session() as session:

            result = await session.execute(select(User).where(User.id == user_id))

            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=401, detail='Invalid credentials')
            
            music_genre = user.favorite_music_genre

            if not music_genre:
                music_genre = 'You gotta generate at least one recommendation to verify your verify your favorite music genre'

            return ProfileResponse(username=user.username, email=user.email, favorite_music_genre=music_genre)

