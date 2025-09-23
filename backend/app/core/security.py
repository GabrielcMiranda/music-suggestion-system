from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from os import getenv
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = getenv('SECRET')
ALGORITHM = getenv('ALGORITHM')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')