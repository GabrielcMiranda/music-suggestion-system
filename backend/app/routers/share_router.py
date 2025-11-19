from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ShareProfileRequest, StandartOutput, UserMusic 
from app.services.auth_service import AuthService
from app.services.share_service import ShareService
from app.core.database.connection import async_session
from app.models import User
from sqlalchemy.future import select
from uuid import UUID

share_router = APIRouter(prefix='/share', tags=['Share'])

@share_router.post('/song', response_model=StandartOutput)
async def share_music_email(
    share_request: UserMusic,
    recipient_email: str,
    current_user_id: UUID = Depends(AuthService.validate_user_auth)
):  
    # buscar dados do usuário logado (quem vai enviar)
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == current_user_id))
        sender_user = result.scalar_one_or_none()
        
        if not sender_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # serviço para enviar o email
    return await ShareService.share_music_by_email(
        dto=share_request,
        sender_username=sender_user.username,  # nome do usuário logado
        recipient_email=recipient_email
    )
    
@share_router.post('/profile', response_model=StandartOutput)
async def share_profile_email(
    share_request: ShareProfileRequest,
    current_user_id: UUID = Depends(AuthService.validate_user_auth)
):  
    # dados completos do usuário logado
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == current_user_id))
        sender_user = result.scalar_one_or_none()
        
        if not sender_user:
            raise HTTPException(status_code=404, dsetail="Usuário não encontrado")
    
    # serviço para enviar o email do perfil
    return await ShareService.share_profile_by_email(
        dto=share_request,
        sender_username=sender_user.username,
        sender_favorite_genre=sender_user.favorite_music_genre or "Não definido",
        sender_profile_picture=sender_user.profile_picture
    )   