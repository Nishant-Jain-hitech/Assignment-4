from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base, SessionLocal, engine
# from config import DATABASE_URL
from datetime import datetime


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))

    teacher_profile = relationship(
        "TeacherProfile",
        back_populates="teacher",
        uselist=False,
        cascade="all, delete-orphan",
    )

    department = relationship("Department", back_populates="teacher")


class TeacherProfile(Base):
    __tablename__ = "teachers_profile"

    id = Column(Integer, primary_key=True, index=True)
    qualification = Column(String)
    experience_years = Column(Integer)

    teacher_id = Column(
        Integer, ForeignKey("teachers.id", ondelete="CASCADE"), unique=True
    )

    teacher = relationship("Teacher", back_populates="teacher_profile")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    teacher = relationship("Teacher", back_populates="department")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    enrollments = relationship(
        "Enrollment", back_populates="student", cascade="all, delete-orphan"
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    credits = Column(Integer)

    enrollments = relationship(
        "Enrollment", back_populates="course", cascade="all, delete-orphan"
    )


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    semester = Column(Integer)
    enrolled_at = Column(DateTime, default=datetime.now())

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
