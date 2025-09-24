from fastapi import APIRouter, HTTPException
from app.services.auth_service import AuthService
from app.schemas import Token, LoginRequest, RegisterRequest, StandartOutput


auth_router = APIRouter(prefix='/auth')

@auth_router.post('/login', tags=['Auth'], response_model=Token)
async def login(dto: LoginRequest):
    try:
        return await AuthService.login(dto)
    except HTTPException as error:
        raise HTTPException(error.status_code, error.detail)

@auth_router.post('/register',tags=['Auth'])
async def register(dto:RegisterRequest):
    try:
        await AuthService.register(dto)
        return StandartOutput(status_code= 200, detail='user created sucessfully')
    except HTTPException as error:
        raise HTTPException(error.status_code, error.detail)