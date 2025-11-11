from fastapi import APIRouter, HTTPException
from app.services.auth_service import AuthService
from app.schemas import Token, LoginRequest, RegisterRequest, StandartOutput
import logging


auth_router = APIRouter(prefix='/auth')

@auth_router.post('/login', tags=['Auth'], response_model=Token)
async def login(dto: LoginRequest):

    try:
        return await AuthService.login(dto)
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')

@auth_router.post('/register',tags=['Auth'])
async def register(dto:RegisterRequest):

    try:
        return await AuthService.register(dto)
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later')