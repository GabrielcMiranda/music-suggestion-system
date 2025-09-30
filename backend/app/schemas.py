from pydantic import BaseModel
class LoginRequest(BaseModel):
    login:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class RegisterRequest(BaseModel):
    username:str
    email:str
    password:str

class ProfileResponse(BaseModel):
    username:str
    email:str
    favorite_music_genre:str
    profile_picture:str | None = None

class OtherProfileResponse(BaseModel):
    username:str
    favorite_music_genre:str
    profile_picture:str | None = None

class StandartOutput(BaseModel):
    status_code:int
    detail:str