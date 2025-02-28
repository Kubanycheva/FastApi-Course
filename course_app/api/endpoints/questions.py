
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from course_app.db.database import SessionLocal
from course_app.db.models import Question
from sqlalchemy.orm import Session

from course_app.db.schema import QuestionSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

questions_router = APIRouter(prefix='/category', tags=['Questions'])


@questions_router.post('/question/create/', response_model=QuestionSchema)
async def create_questions(question: QuestionSchema, db: Session = Depends(get_db)):
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@questions_router.get('/question/', response_model=List[QuestionSchema])
async def list_question(db: Session = Depends(get_db)):
    return db.query(Question).all()


@questions_router.get('/question/{question_id}/', response_model=QuestionSchema)
async def detail_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='Question Not Found')
    return question


@questions_router.put('/question/{question_id}/', response_model=QuestionSchema)
async def update_question(question_id: int, question_data: QuestionSchema,
                          db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='Question Not Found')
    return question

    for question_key, question_value in question_data.dict().items():
        setattr(question, question_key, question_value)
    db.commit()
    db.refresh(question)
    return question


@questions_router.delete('/{user_id}/')
async def delete_questions(questions_id: int, db: Session = Depends(get_db)):
    questions = db.query(Question).filter(Question.id == questions_id).first()
    if questions is None:
        raise HTTPException(status_code=404, detail='Questions Not Found')
    db.delete(questions)
    db.commit()
    return {'message': 'This questions is deleted'}