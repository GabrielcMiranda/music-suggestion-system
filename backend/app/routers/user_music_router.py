from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserMusicHistoryResponse, UserMusic, StandartOutput, RecommendationRequest
from app.services.auth_service import AuthService
from app.services.user_music_service import UserMusicService
import logging
from typing import List
from fastapi import Body
from uuid import UUID

user_music_router = APIRouter(prefix='/my-musics', tags=['User Musics'])

@user_music_router.post('/recommend', response_model=StandartOutput)
async def recommend_music(dto:RecommendationRequest , user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        await UserMusicService.make_recommendation(user_id, dto.music_input)
        return StandartOutput(status_code=200, detail='Music recommendation generated successfully.')
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error("Error in recommend_music: %s", error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')

@user_music_router.get('/', response_model=UserMusicHistoryResponse)
async def get_my_musics(
    current_user_id: UUID = Depends(AuthService.validate_user_auth)
):
    """
    Retorna todas as músicas recomendadas para o usuário logado,
    agrupadas por recomendação
    """
    return await UserMusicService.get_user_musics(current_user_id)

@user_music_router.get('/all', response_model=List[UserMusic])
async def get_all_my_musics(
    current_user_id: UUID = Depends(AuthService.validate_user_auth)
):
    """
    Retorna todas as músicas do usuário em uma lista simples
    (sem agrupar por recomendação)
    """
    return await UserMusicService.get_all_user_musics_flat(current_user_id)

@user_music_router.get('/recommendation/{recommendation_id}', response_model=List[UserMusic])
async def get_musics_from_recommendation(
    recommendation_id: int,
    current_user_id: UUID = Depends(AuthService.validate_user_auth)
):
    """
    Retorna as músicas de uma recomendação específica do usuário
    """
    return await UserMusicService.get_musics_by_recommendation(
        user_id=current_user_id,
        recommendation_id=recommendation_id
    )