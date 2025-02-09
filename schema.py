from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models import UserRole, StatusCourse, TypeCourse


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    phone_number: Optional[str] = None
    age: Optional[int] = None
    profile_picture: Optional[str] = None
    role: UserRole


class CategorySchema(BaseModel):
    id: int
    category_name: str


class CourseSchema(BaseModel):
    id: int
    course_name: str
    description: str
    level: StatusCourse
    price: float
    type_course: TypeCourse
    created_at: datetime
    updated_at: datetime
    author_id: int

    class Config:
        from_attributes = True


class LessonSchema(BaseModel):
    id: int
    title: str
    video_url: Optional[str] = None
    content: Optional[str] = None
    course_id: int


class ExamSchema(BaseModel):
    id: int
    title: str
    course_id: int
    end_time: int


class QuestionSchema(BaseModel):
    id: int
    exam_id: int
    title: str
    score: int


class CertificateSchema(BaseModel):
    id: int
    student_id: int
    course_id: int
    issued_at: datetime
    certificate_url: str