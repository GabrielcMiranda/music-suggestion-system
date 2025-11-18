from pydantic import BaseModel
from typing import List

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
    
class ShareProfileRequest(BaseModel):
    recipient_email:str
    message:str | None = None
    
class UserMusic(BaseModel):
    title: str
    artist: str
    genre: str | None = None
    album: str | None = None

class UserMusicHistory(BaseModel):
    recommendation_id: int
    song_input: str
    musics: List[UserMusic]

class UserMusicHistoryResponse(BaseModel):
    user_musics: List[UserMusicHistory]

class RecommendationRequest(BaseModel):
    music_input: str

class RecommendationResponse(BaseModel):
    recommendations: List[UserMusic]