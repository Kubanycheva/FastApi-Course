from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from course_app.db.database import SessionLocal
from course_app.db.models import Exam
from sqlalchemy.orm import Session

from course_app.db.schema import ExamSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

exam_router = APIRouter(prefix='/exam', tags=['Exam'])


@exam_router.post('/create/', response_model=ExamSchema)
async def create_exam(exam: ExamSchema, db: Session = Depends(get_db)):
    db_exam = Exam(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


@exam_router.get('/', response_model=List[ExamSchema])
async def list_exam(db: Session = Depends(get_db)):
    return db.query(Exam).all()


@exam_router.get('/{exam_id}/', response_model=ExamSchema)
async def detail_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail='Exam Not Found')
    return exam


@exam_router.put('/{exam_id}/',response_model=ExamSchema)
async def update_exam(exam_id: int, exam_data: ExamSchema,
                        db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail='Exam Not Found')
    return exam

    for exam_key, exam_value in exam_data.dict().items():
        setattr(exam, exam_key, exam_value)
    db.commit()
    db.refresh(exam)
    return exam


@exam_router.delete('/exam/{exam_id}/', summary='Экзамен удаления')
async def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail='Exam Not Found')
    db.delete(exam)
    db.commit()
    return {'message': 'This exam is deleted'}
