from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = '8fcc241573ab002305fb5e0bb2e647fc12c6a30beacb36d027b072ce1fbe4da0'
ACCESS_TOKEN_EXPIRE_MINUTES = 40
REFRESH_TOKEN_EXPIRE_DAYS = 3
ALGORITHM = 'HS256'

