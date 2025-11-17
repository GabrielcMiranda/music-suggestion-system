from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import desc
import asyncio
from app.core.database.connection import async_session
from collections import Counter
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
            recommendation = Recommendation(musicas=songs, song_input=music_input)
            user.recommendations.append(recommendation)
            session.add(user)

            await session.commit()
            await session.refresh(recommendation)

            musics = []
            for song in songs:
                if isinstance(song, dict):
                    music = UserMusic(
                        title=song.get('title', 'Título não informado'),
                        artist=song.get('artist', 'Artista não informado'),
                        genre=song.get('genre', 'Gênero não informado'),
                        album=song.get('album', 'Álbum não informado'),
                    )
                    musics.append(music)

            return musics

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

            if not recommendations:
                raise HTTPException(status_code=404, detail="No recommendations found for this user.")
            
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
                        song_input=recommendation.song_input,
                        musics=musics
                    )
                    user_musics.append(user_music_history)
            
            return UserMusicHistoryResponse(
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

            if not recommendations:
                raise HTTPException(status_code=404, detail="No recommendations found for this user.")
            
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
    async def count_recommendations(user_id: UUID, by: str):
        async with async_session() as session:
            user_result = await session.execute(
                select(User).options(selectinload(User.recommendations)).where(User.id == user_id)
            )
            user = user_result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            query = select(Recommendation).where(Recommendation.user_id == user_id)
            rec_result = await session.execute(query)
            recommendations = rec_result.scalars().all()

            if not recommendations:
                raise HTTPException(status_code=404, detail="No recommendations found for this user.")

            contador = Counter()

            for rec in user.recommendations:
                if rec.musicas:  # lista de músicas (JSON)
                    for musica in rec.musicas:
                        chave = None
                        if by == "artist":
                            chave = musica.get("artist")
                        elif by == "music_title":
                            chave = musica.get("title")
                        if chave:
                            contador[chave] += 1

            return dict(contador)
    
    @staticmethod
    async def get_favorite_genre(user_id: UUID) -> str:
        """Calcula o gênero musical mais frequente nas recomendações do usuário"""
        async with async_session() as session:
            query = select(Recommendation).where(Recommendation.user_id == user_id)
            result = await session.execute(query)
            recommendations = result.scalars().all()

            if not recommendations:
                return None 
            
            genre_counter = Counter()

            for rec in recommendations:
                if rec.musicas:  
                    for musica in rec.musicas:
                        genre = musica.get("genre")
                        if genre:
                            genre_counter[genre] += 1
            
            if not genre_counter:
                return None  
            
            return genre_counter.most_common(1)[0][0]