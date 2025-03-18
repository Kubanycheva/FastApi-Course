from sqlalchemy import Integer, String, ForeignKey, DateTime, Text, DECIMAL, Enum, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from course_app.db.database import Base
from enum import Enum as PyEnum
from passlib.hash import bcrypt


course_user = Table('course_user', Base.metadata,
                    Column('user_id', ForeignKey('user_profiles.id'), primary_key=True),
                    Column('course_id', ForeignKey('courses.id'), primary_key=True))


class UserRole(str, PyEnum):
    teacher = 'teacher'
    student = 'student'


class StatusCourse(str, PyEnum):
    level1 = 'легкий'
    level2 = 'средний'
    level3 = 'сложный'


class TypeCourse(str, PyEnum):
    type1 = 'бесплатный'
    type2 = 'платный'


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(40), unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    profile_picture: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.student)

    course: Mapped["Course"] = relationship("Course", back_populates="author", secondary=course_user)

    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                        cascade='all, delete-orphan')

    cart_user:  Mapped['Cart'] = relationship('Cart', back_populates='users', cascade='all, delete-orphan',
                                              uselist=False)
    # favorite_user: Mapped['Favorite'] = relationship('Favorite', back_populates='users', cascade='all, delete_orphan',
    #                                                  uselist=False)

    def set_passwords(self, password: str):
        self.hashed_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

    def __str__(self):
        return self.username


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'), unique=True)
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String, unique=True, index=True)

    def __repr__(self):
        return self.category_name


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    level: Mapped[StatusCourse] = mapped_column(Enum(StatusCourse), nullable=False)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(8, 2))
    type_course: Mapped[TypeCourse] = mapped_column(Enum(TypeCourse), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author: Mapped['UserProfile'] = relationship('UserProfile', back_populates='course', secondary=course_user)


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    video_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    end_time: Mapped[int] = mapped_column(Integer)


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"))
    title: Mapped[str] = mapped_column(String, index=True)
    score: Mapped[int] = mapped_column(Integer)


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    certificate_url: Mapped[str] = mapped_column(String)


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    users: Mapped['UserProfile'] = relationship('UserProfile',
                                                back_populates='cart_user')

    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')

    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    course: Mapped['Course'] = relationship('Course')


# class Favorite(Base):
#     __tablename__ = 'favorite'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     favorite_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
#     favorites: Mapped['UserProfile'] = relationship('UserProfile', back_populates='favorite_user')
#
#
# class FavoriteItem(Base):
#     __tablename__ = 'favorite_item'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     favorite_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))

