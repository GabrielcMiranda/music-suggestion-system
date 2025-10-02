from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserMusicHistoryResponse, UserMusic
from app.services.auth_service import AuthService
from app.services.user_music_service import UserMusicService
from typing import List
from uuid import UUID

user_music_router = APIRouter(prefix='/my-musics', tags=['User Musics'])

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