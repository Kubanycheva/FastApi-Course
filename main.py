import fastapi
from models import Category
from schema import CategorySchema
from database import SessionLocal
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schema import *


course_app = fastapi.FastAPI(title='Course Site')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@course_app.post('/category/create', response_model=CategorySchema)
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    db_category = Category(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@course_app.get('/category/', response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()
