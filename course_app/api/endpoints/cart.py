from course_app.db.models import Cart, CartItem, Course
from course_app.db.schema import CartSchema, CartItemSchema, CourseSchema
from fastapi import APIRouter, Depends, HTTPException
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session

cart_router = APIRouter(prefix='/cart', tags=['Cart'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@cart_router.get('/', response_model=CartSchema)
async def cart_list(user_id: int, db: Session=Depends(get_db)):
xxx`
