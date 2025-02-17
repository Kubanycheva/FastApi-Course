import fastapi
from models import Category, Course, Lesson, Exam, Question, Certificate, UserProfile
from schema import CategorySchema, CourseSchema, LessonSchema, ExamSchema, QuestionSchema, CertificateSchema, UserProfileSchema
from database import SessionLocal
from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional
from schema import *
from config import (SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES,
                    REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM)
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime


course_app = fastapi.FastAPI(title='Course Site')

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


@course_app.post('/register')
async def register(user: UserProfileSchema,  db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if user_db:
        raise HTTPException(status_code=400, detail='username бар экен')
    new_hash_pass = get_password_hash(user.password)
    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        age=user.age,
        profile_picture=user.profile_picture,
        role=user.role,
        hashed_password=new_hash_pass
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'Saved'}


@course_app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Маалымат туура эмес')
    access_token = create_access_token({'sub': user.username})
    refresh_token = create_refresh_token({'sub': user.username})
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type':'bearer'}


@course_app.post('/logout')
async def logout():
    return {'message': 'Вышли'}


@course_app.post('/category/create/', response_model=CategorySchema, summary='Категория создания', tags=['Категории'])
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    db_category = Category(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category



@course_app.get('/category/', response_model=List[CategorySchema], summary='Категория получения информации', tags=['Категории'])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@course_app.get('/category/{category_id}/', response_model=CategorySchema, summary='Категория детайл', tags=['Категории'])
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id==category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    return category


@course_app.put('/category/{category_id}/', response_model=CategorySchema, summary='Категория изменения', tags=['Категории'])
async def update_category(category_id: int, category_data: CategorySchema,
                          db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    category.category_name=category_data.category_name
    db.commit()
    db.refresh(category)
    return category


@course_app.delete('/category/{category_id}/', summary='Категория удаления', tags=['Категории'])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    db.delete(category)
    db.commit()
    return {"message": 'This product id deleted'}


@course_app.post('/course/create/', response_model=CourseSchema, summary='Курс создании', tags=['Курс'])
async def create_course(course: CourseSchema, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@course_app.get('/course/', response_model=List[CourseSchema], summary='Курс получения информации', tags=['Курс'])
async def list_course(db: Session = Depends(get_db)):
    return db.query(Course).all()


@course_app.get('/course/{course_id}/', response_model=CourseSchema, summary='Курс детайл', tags=['Курс'])
async def detail_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    return course


@course_app.put('/course/{course_id}/', response_model=CourseSchema, summary='Курс изменения', tags=['Курс'])
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


@course_app.delete('/course/{course_id}/', summary='Курс удаления', tags=['Курс'])
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    db.delete(course)
    db.commit()
    return {'message': 'This course is deleted'}


@course_app.post('/lesson/create/', response_model=LessonSchema, summary='Урок создании', tags=['Уроки'])
async def create_lesson(lesson: LessonSchema, db: Session = Depends(get_db)):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


@course_app.get('/lesson/', response_model=List[LessonSchema],  summary='Урок получения информации', tags=['Уроки'])
async def list_lesson(db: Session = Depends(get_db)):
    return db.query(Lesson).all()


@course_app.get('/lesson/{lesson_id}/', response_model=LessonSchema,  summary='Урок детайл', tags=['Уроки'])
async def detail_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail='Lesson Not Found')
    return lesson


@course_app.put('/lesson/{lesson_id}/',response_model=LessonSchema,  summary='Урок изменения', tags=['Уроки'])
async def update_lesson(lesson_id: int, lesson_data: LessonSchema,
                        db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail='Lesson Not Found')
    return lesson

    for lesson_key, lesson_value in lesson_data.dict().items():
        setattr(lesson, lesson_key, lesson_value)
    db.commit()
    db.refresh(lesson)
    return lesson


@course_app.delete('/lesson/{lesson_id}/',  summary='Урок удаления', tags=['Уроки'])
async def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail='Lesson Not Found')
    db.delete(lesson)
    db.commit()
    return {'message': 'This lesson is deleted'}


@course_app.post('/exam/create/', response_model=ExamSchema,  summary='Экзамен создании', tags=['Экзамены'])
async def create_exam(exam: ExamSchema, db: Session = Depends(get_db)):
    db_exam = Exam(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


@course_app.get('/exam/', response_model=List[ExamSchema], summary='Экзамен получения информации', tags=['Экзамены'])
async def list_exam(db: Session = Depends(get_db)):
    return db.query(Exam).all()


@course_app.get('/exam/{exam_id}/', response_model=ExamSchema,  summary='Экзамен детайл', tags=['Экзамены'])
async def detail_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail='Exam Not Found')
    return exam


@course_app.put('/exam/{exam_id}/',response_model=ExamSchema,   summary='Экзамен изменения', tags=['Экзамены'])
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


@course_app.delete('/exam/{exam_id}/', summary='Экзамен удаления', tags=['Экзамены'])
async def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail='Exam Not Found')
    db.delete(exam)
    db.commit()
    return {'message': 'This exam is deleted'}


@course_app.post('/question/create/', response_model=QuestionSchema, tags=['Вопросы'])
async def create_questions(question: QuestionSchema, db: Session = Depends(get_db)):
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@course_app.get('/question/', response_model=List[QuestionSchema], tags=['Вопросы'])
async def list_question(db: Session = Depends(get_db)):
    return db.query(Question).all()


@course_app.get('/question/{question_id}/', response_model=QuestionSchema, tags=['Вопросы'])
async def detail_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='Question Not Found')
    return question


@course_app.put('/question/{question_id}/', response_model=QuestionSchema, tags=['Вопросы'])
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


@course_app.post('/certificate/create/', response_model=CertificateSchema, tags=['Сертификаты'])
async def create_certificate(certificate: CertificateSchema, db: Session = Depends(get_db)):
    db_certificate = Certificate(**certificate.dict())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate


@course_app.get('/certificate/', response_model=List[CertificateSchema], tags=['Сертификаты'])
async def list_certificate(db: Session = Depends(get_db)):
    return db.query(Certificate).all()


@course_app.get('/certificate/{certificate_id}', response_model=CertificateSchema, tags=['Сертификаты'])
async def detail_certificate(certificate_id: int, db: Session = Depends(get_db)):
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail='Certificate Not Found')
    return certificate


@course_app.put('/certificate/{certificate_id}', response_model=CertificateSchema, tags=['Сертификаты'])
async def update_certificate(certificate_id: int, certificate_data: CertificateSchema,
                             db: Session = Depends(get_db)):
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail='Certificate Not Found')

    for certificate_key, certificate_value in certificate_data.dict().items():
        setattr(certificate, certificate_key, certificate_value)

    db.commit()
    db.refresh(certificate)
    return certificate


@course_app.delete('/certificate{certificate_id}/', tags=['Сертификаты'])
async def delete_certificate(certificate_id: int,   db: Session = Depends(get_db)):
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail='Certificate Not Found')
    db.delete(certificate)
    db.commit()
    return {'message': 'This certificate  is deleted'}






