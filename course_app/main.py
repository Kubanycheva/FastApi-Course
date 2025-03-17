from starlette.middleware.sessions import SessionMiddleware
import fastapi
from fastapi import FastAPI
from api.endpoints import auth, categories, courses, users, lessons, exams, questions, certificates, social_auth, cart

import redis.asyncio as redis
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from sqladmin import Admin, ModelView

import uvicorn

from course_app.admin.setup import setup_admin


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8',
                                decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


course_app = fastapi.FastAPI(title='Course Site', lifespan=lifespan)

course_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")

setup_admin(course_app)

course_app.include_router(auth.auth_router)
course_app.include_router(users.users_router)
course_app.include_router(categories.category_router)
course_app.include_router(courses.course_router)
course_app.include_router(lessons.lessons_router)
course_app.include_router(exams.exam_router)
course_app.include_router(questions.questions_router)
course_app.include_router(certificates.certificate_router)
course_app.include_router(social_auth.social_router)
course_app.include_router(cart.cart_router)

if __name__ == '__main__':
    uvicorn.run(course_app, host='127.0.0.1', port=8000)


