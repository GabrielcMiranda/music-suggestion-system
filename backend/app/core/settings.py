from os import getenv
from dotenv import load_dotenv

class Settings:

    load_dotenv()
    SECRET_KEY = getenv('SECRET_KEY')
    ALGORITHM = getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    PG_URL = getenv('PG_URL')
    SMTP_SERVER = getenv('SMTP_SERVER')
    SMTP_PORT = getenv('SMTP_PORT')
    EMAIL_USER = getenv('EMAIL_USER')
    EMAIL_PASSWORD = getenv('EMAIL_PASSWORD')
    FRONTEND_URL = getenv('FRONTEND_URL')