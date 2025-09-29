import logging
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ProfileResponse, OtherProfileResponse
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from uuid import UUID

user_router = APIRouter(prefix='/user')

from typing import Union

@user_router.get('/{username}/profile', tags=['User'], response_model=Union[ProfileResponse, OtherProfileResponse])
async def get_profile(username: str, user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        return await UserService.get_profile(username, user_id)
    
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')