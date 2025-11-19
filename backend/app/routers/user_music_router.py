from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserMusicHistoryResponse, UserMusic, StandartOutput, RecommendationRequest, RecommendationResponse
from app.services.auth_service import AuthService
from app.services.user_music_service import UserMusicService
import logging
from typing import List
from fastapi import Query
from uuid import UUID

user_music_router = APIRouter(prefix='/my-musics', tags=['User Musics'])

@user_music_router.post('/recommend', response_model=RecommendationResponse)
async def recommend_music(dto:RecommendationRequest , user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        recommendations = await UserMusicService.make_recommendation(user_id, dto.music_input)
        return RecommendationResponse(recommendations=recommendations)
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error("Error in recommend_music: %s", error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')

@user_music_router.get('/', response_model=UserMusicHistoryResponse)
async def get_my_musics(
    page: int = Query(1, ge=1, description="Número da página (começa em 1)"),
    page_size: int = Query(10, ge=1, le=50, description="Quantidade de recomendações por página"),
    current_user_id: UUID = Depends(AuthService.validate_user_auth)
):
    """
    Retorna as músicas recomendadas para o usuário logado,
    agrupadas por recomendação, com paginação
    """
    return await UserMusicService.get_user_musics(current_user_id, page, page_size)

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

@user_music_router.get("/stats")
async def count_recommendations(
    user_id: UUID = Depends(AuthService.validate_user_auth),
    by: str = Query("artist", regex="^(artist|genre)$")
):
    try:
        return await UserMusicService.count_recommendations(user_id, by)

    except HTTPException as error:
            raise error
    except Exception as error:
        logging.error("Error in recommend_music: %s", error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')
