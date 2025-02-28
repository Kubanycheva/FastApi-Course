from sqladmin import ModelView
from course_app.db.models import (UserProfile, Category,
                                  Course, Certificate, Exam, Question, Lesson)


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.role]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.course_name]


class CertificateAdmin(ModelView, model=Certificate):
    column_list = [Certificate.id, Certificate.certificate_url]


class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.title]


class ExamAdmin(ModelView, model=Exam):
    column_list = [Exam.id, Exam.title]


class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.id, Lesson.title]



