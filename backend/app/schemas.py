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

class StandartOutput(BaseModel):
    status_code:int
    detail:str