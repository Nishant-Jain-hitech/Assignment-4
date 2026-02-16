from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ResponseSchemas import DepartmentResponse, TeacherResponse, StudentResponse, CourseResponse, EnrollmentResponse
from CreateSchemas import DepartmentModel, TeacherModel, StudentModel, CourseModel, EnrollmentModel
from models import get_db, Department, Teacher, TeacherProfile, Student, Course, Enrollment

router=APIRouter()


@router.get("/")
def read_root():
    return {"message":"Han bhai aa gya"}


@router.post("/departments", response_model=DepartmentResponse)
def create_department(department:DepartmentModel, db:Session=Depends(get_db)):
    db_department=Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.post("/teachers", response_model=TeacherResponse)
def create_teacher(teacher:TeacherModel, db:Session=Depends(get_db)):
    db_teacher=Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher
    


@router.post("/students", response_model=StudentResponse)
def create_student(student:StudentModel,db:Session=Depends(get_db)):
    db_student=Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.post("/courses", response_model=CourseResponse)
def create_course(course:CourseModel,db:Session=Depends(get_db)):
    db_course=Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.post("/enrollments", response_model=EnrollmentResponse)
def create_enrollment(enrollment:EnrollmentModel,db:Session=Depends(get_db)):
    db_enrollment=Student(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment
    