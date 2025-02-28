from fastapi import FastAPI
from sqladmin import Admin
from .views import (UserProfileAdmin, CategoryAdmin,
                    CourseAdmin, CertificateAdmin, ExamAdmin, LessonAdmin, QuestionAdmin)
from course_app.db.models import (UserProfile, Category,
                                  Course, Certificate, Lesson, Exam, Question)
from course_app.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(CourseAdmin)
    admin.add_view(CertificateAdmin)
    admin.add_view(ExamAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(QuestionAdmin)
