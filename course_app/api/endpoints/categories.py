from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from course_app.db.database import SessionLocal
from course_app.db.models import Category
from sqlalchemy.orm import Session

from course_app.db.schema import CategorySchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

category_router = APIRouter(prefix='/category', tags=['Category'])


@category_router.post('/create/', response_model=CategorySchema)
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    db_category = Category(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@category_router.get('/', response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get('/{category_id}/', response_model=CategorySchema)
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id==category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    return category


@category_router.put('/{category_id}/', response_model=CategorySchema)
async def update_category(category_id: int, category_data: CategorySchema,
                          db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    category.category_name=category_data.category_name
    db.commit()
    db.refresh(category)
    return category


@category_router.delete('/{category_id}/')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    db.delete(category)
    db.commit()
    return {"message": 'This product id deleted'}