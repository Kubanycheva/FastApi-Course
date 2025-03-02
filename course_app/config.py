from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 40
REFRESH_TOKEN_EXPIRE_DAYS = 3
ALGORITHM = 'HS256'


class Settings:
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_KEY = os.getenv('GITHUB_KEY')
    GITHUB_URL = os.getenv('GITHUB_URL')

settings = Settings()