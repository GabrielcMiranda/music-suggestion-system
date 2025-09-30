import logging
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from app.schemas import ProfileResponse, OtherProfileResponse, StandartOutput
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.file_service import FileService
from uuid import UUID
from typing import Union

user_router = APIRouter(prefix='/user')

@user_router.get('/{username}/profile', tags=['User'], response_model=Union[ProfileResponse, OtherProfileResponse])
async def get_profile(username: str, user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        return await UserService.get_profile(username, user_id)
    
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')
    
@user_router.patch('/profile/change-picture', tags=['User'], response_model=StandartOutput)
async def change_profile_picture(file:UploadFile = File(...) , user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        url = await FileService.upload_image(file, str(user_id))
        await UserService.update_profile_picture(user_id, url)
        return StandartOutput(status_code=200, detail='Profile picture updated successfully.')
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')