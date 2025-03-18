from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from course_app.db.database import SessionLocal
from course_app.db.models import Course, StatusCourse, TypeCourse
from course_app.db.schema import CourseSchema

from sqlalchemy import asc, desc

from fastapi_pagination import Page, add_pagination, paginate
course_router = APIRouter(prefix='/course', tags=['Course'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@course_router.get('/search/', response_model=List[CourseSchema])
async def search_course(course_name: str, db: Session = Depends(get_db)):
    course_db = db.query(Course).filter(Course.course_name.ilike(f'%{course_name}%')).all()
    if course_db is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    return course_db


@course_router.post('/create/', response_model=CourseSchema)
async def create_course(course: CourseSchema, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


@course_router.get('/', response_model=Page[CourseSchema])
async def list_course(min_price: Optional[float] = Query(None, alias='price[from]'),
                      max_price: Optional[float] = Query(None, alias='price[to]'),
                      level: Optional[StatusCourse] = None,
                      type_course: Optional[TypeCourse] = None,
                      order_by: Optional[str] = Query(None, regex='^(asc|desc)$'),
                      db: Session = Depends(get_db)):
    query = db.query(Course)

    if min_price is not None:
        query = query.filter(Course.price >= min_price)

    if max_price is not None:
        query = query.filter(Course.price <= max_price)
        
    if level is not None:
        query = query.filter(Course.level == level)

    if type_course:
        query = query.filter(Course.type_course == type_course)

    if order_by == 'asc':
        query = query.order_by(asc(Course.price))
    elif order_by == 'desc':
        query = query.order_by(desc(Course.price))

    courses = query.all()

    if not courses:
        raise HTTPException(status_code=404, detail='Courses Not Found')

    return paginate(courses)


@course_router.get('/{course_id}/', response_model=CourseSchema)
async def detail_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    return course


@course_router.put('/{course_id}/', response_model=CourseSchema)
async def update_course(course_id: int, course_data: CourseSchema,
                        db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    return course

    for course_key, course_value in course_data.dict().items():
        setattr(course, course_key, course_value)
    db.commit()
    db.refresh(course)
    return course


@course_router.delete('/{course_id}/', summary='Курс удаления')
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    db.delete(course)
    db.commit()
    return {'message': 'This course is deleted'}

