from starlette.requests import Request
from course_app.db.database import SessionLocal
from authlib.integrations.starlette_client  import OAuth
from course_app.config import settings
from fastapi import APIRouter

social_router = APIRouter(prefix='/oauth', tags=['SocialOAuth'])


oauth = OAuth()
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    secret_key=settings.GITHUB_KEY,
    authorize_url='https://github.com/login/oauth/authorize',

)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@social_router.get('/login/github')
async def github_login(request: Request):
    redirect_uri = settings.GITHUB_URL
    return await oauth.github.authorize_redirect(request, redirect_uri)
