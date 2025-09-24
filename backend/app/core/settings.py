from os import getenv
from dotenv import load_dotenv

class Settings:

    load_dotenv()
    SECRET_KEY = getenv('SECRET_KEY')
    ALGORITHM = getenv('ALGORITHM')
    PG_URL = getenv('PG_URL')