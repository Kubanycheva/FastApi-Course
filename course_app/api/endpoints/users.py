from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from course_app.db.database import SessionLocal
from course_app.db.models import UserProfile
from course_app.db.schema import UserProfileSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

users_router = APIRouter(prefix='/users', tags=['UserProfile'])


@users_router.post('/create', response_model=UserProfileSchema)
async def create_user(user: UserProfileSchema, db: Session = Depends(get_db)):
    db.user = UserProfile(**user.dict())
    db.add(db.user)
    db.commit()
    db.refresh(db.user)
    return db.user


@users_router.get('/', response_model=UserProfileSchema)
async def list_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@users_router.get('/{user.id}/', response_model=UserProfileSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    return user


@users_router.put('/{user_id}/', response_model=UserProfileSchema)
async def update_user(user_id: int, user_data: UserProfileSchema, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    return user

    for user_key, user_value in user_data.dict().items():
        setattr(user, user_key, user_value)
    db.commit()
    db.refresh(user)
    return user


@users_router.delete('/{user_id}/')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    db.delete(user)
    db.commit()
    return {'message': 'This user is deleted'}


