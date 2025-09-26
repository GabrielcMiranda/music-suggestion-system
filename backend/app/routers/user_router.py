from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ProfileResponse
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from uuid import UUID

user_router = APIRouter(prefix='/user')

@user_router.get('/profile', tags=['User'], response_model=ProfileResponse)
async def get_profile(user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        return await UserService.get_profile(user_id)
    
    except HTTPException as error:
        raise error
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')