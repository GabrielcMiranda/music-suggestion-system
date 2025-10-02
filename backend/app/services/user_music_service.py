from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import desc
import asyncio
from app.core.database.connection import async_session
from app.services.recommendationDA.data import recomendar_musicas
from app.models import Recommendation, User
from app.schemas import UserMusic, UserMusicHistory, UserMusicHistoryResponse
from fastapi import HTTPException
from uuid import UUID

class UserMusicService:

    @staticmethod
    async def make_recommendation(user_id: UUID, music_input:str):
        async with async_session() as session:
            result = await session.execute(select(User).options(selectinload(User.recommendations)).where(User.id == user_id))
             
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            songs = await asyncio.to_thread(recomendar_musicas, music_input)

            recommendation = Recommendation(musicas=songs)
            user.recommendations.append(recommendation)

            await session.commit()
            await session.refresh(recommendation)

    
    @staticmethod
    async def get_user_musics(user_id: UUID) -> UserMusicHistoryResponse:
        # retorna todas as músicas recomendadas para o usuário
        async with async_session() as session:
            # Buscar todas as recomendações do usuário
            query = (
                select(Recommendation)
                .where(Recommendation.user_id == user_id)
                .order_by(desc(Recommendation.id))
            )
            
            result = await session.execute(query)
            recommendations = result.scalars().all()
            
            user_musics = []
            total_musics = 0
            
            for recommendation in recommendations:
                musicas_data = recommendation.musicas if isinstance(recommendation.musicas, list) else []
                
                # Converter para objetos UserMusic
                musics = []
                for musica_dict in musicas_data:
                    if isinstance(musica_dict, dict):
                        music = UserMusic(
                            title=musica_dict.get('title', 'Título não informado'),
                            artist=musica_dict.get('artist', 'Artista não informado'),
                            genre=musica_dict.get('genre'),
                            album=musica_dict.get('album'),
                        )
                        musics.append(music)
                
                if musics:  # Só adiciona se tiver músicas
                    user_music_history = UserMusicHistory(
                        recommendation_id=recommendation.id,
                        musics=musics
                    )
                    user_musics.append(user_music_history)
                    total_musics += len(musics)
            
            return UserMusicHistoryResponse(
                total_recommendations=len(user_musics),
                total_musics=total_musics,
                user_musics=user_musics
            )
    
    @staticmethod
    async def get_all_user_musics_flat(user_id: UUID) -> List[UserMusic]:
        # retorna todas as músicas do usuário em uma lista plana (sem agrupar por recomendação)
        async with async_session() as session:
            # buscar todas as recomendações do usuário
            query = select(Recommendation).where(Recommendation.user_id == user_id)
            result = await session.execute(query)
            recommendations = result.scalars().all()
            
            all_musics = []
            
            for recommendation in recommendations:
                musicas_data = recommendation.musicas if isinstance(recommendation.musicas, list) else []
                
                for musica_dict in musicas_data:
                    if isinstance(musica_dict, dict):
                        music = UserMusic(
                            title=musica_dict.get('title', 'Título não informado'),
                            artist=musica_dict.get('artist', 'Artista não informado'),
                            genre=musica_dict.get('genre'),
                            album=musica_dict.get('album'),
                        )
                        all_musics.append(music)
            
            return all_musics
    
    @staticmethod
    async def get_musics_by_recommendation(user_id: UUID, recommendation_id: int) -> List[UserMusic]:
        # retorna as músicas de uma recomendação específica do usuário
        async with async_session() as session:
            query = (
                select(Recommendation)
                .where(
                    Recommendation.user_id == user_id,
                    Recommendation.id == recommendation_id
                )
            )
            
            result = await session.execute(query)
            recommendation = result.scalar_one_or_none()
            
            if not recommendation:
                raise HTTPException(
                    status_code=404,
                    detail="Recomendação não encontrada"
                )
            
            musicas_data = recommendation.musicas if isinstance(recommendation.musicas, list) else []
            musics = []
            
            for musica_dict in musicas_data:
                if isinstance(musica_dict, dict):
                    music = UserMusic(
                        title=musica_dict.get('title', 'Título não informado'),
                        artist=musica_dict.get('artist', 'Artista não informado'),
                        genre=musica_dict.get('genre'),
                        album=musica_dict.get('album'),
                    )
                    musics.append(music)
            
            return musics