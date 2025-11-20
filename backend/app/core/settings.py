from os import getenv
import cloudinary
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
    
    RESEND_API_KEY = getenv('RESEND_API_KEY')
    EMAIL_FROM = getenv('EMAIL_FROM', 'Rhythmate <noreply@rhythmate.app>')
    
    FRONTEND_URL = getenv('FRONTEND_URL')

    CLOUDINARY_CLOUD_NAME = getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = getenv('CLOUDINARY_API_SECRET')
    CLOUDINARY_URL = getenv('CLOUDINARY_URL')
    
