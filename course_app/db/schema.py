from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from course_app.db.models import UserRole, StatusCourse, TypeCourse


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    password: str
    phone_number: Optional[str] = None
    age: Optional[int] = None
    profile_picture: Optional[str] = None
    role: UserRole

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True


class CourseSchema(BaseModel):
    id: int
    course_name: str
    description: str
    level: StatusCourse
    price: float
    type_course: TypeCourse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LessonSchema(BaseModel):
    id: int
    title: str
    video_url: Optional[str] = None
    content: Optional[str] = None
    course_id: int

    class Config:
        from_attributes = True


class ExamSchema(BaseModel):
    id: int
    title: str
    course_id: int
    end_time: int

    class Config:
        from_attributes = True


class QuestionSchema(BaseModel):
    id: int
    exam_id: int
    title: str
    score: int

    class Config:
        from_attributes = True


class CertificateSchema(BaseModel):
    id: int
    student_id: int
    course_id: int
    issued_at: datetime
    certificate_url: str

    class Config:
        from_attributes = True


class CartItemSchema(BaseModel):
    id: int
    course_id: int

    class Config:
        from_attributes = True


class CartSchema(BaseModel):
    id: int
    user_id: int
    items: List[CartItemSchema] = []
    total_price: float

    class Config:
        from_attributes = True


class CarItemCreateSchema(BaseModel):
    course_id: int


