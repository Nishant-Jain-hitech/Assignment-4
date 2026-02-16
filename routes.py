from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from ResponseSchemas import (
    DepartmentResponse,
    TeacherResponse,
    StudentResponse,
    CourseResponse,
    EnrollmentResponse,
    GetTeacherResponse,
    GetStudentResponse
)
from CreateSchemas import (
    DepartmentModel,
    TeacherModel,
    StudentModel,
    CourseModel,
    EnrollmentModel,
)
from models import (
    get_db,
    Department,
    Teacher,
    Student,
    Course,
    Enrollment,
    TeacherProfile,
)

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Han bhai aa gya"}


@router.post("/departments", response_model=DepartmentResponse)
def create_department(department: DepartmentModel, db: Session = Depends(get_db)):
    db_department = Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.post("/teachers", response_model=TeacherResponse)
def create_teacher(teacher: TeacherModel, db: Session = Depends(get_db)):
    dept = db.query(Department).filter(Department.id == teacher.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    db_teacher = Teacher(
        name=teacher.name, email=teacher.email, department_id=teacher.department_id
    )

    db_profile = TeacherProfile(
        qualification=teacher.qualification,
        experience_years=teacher.experience_years,
        teacher=db_teacher,
    )

    db.add(db_teacher)
    db.add(db_profile)
    db.commit()
    db.refresh(db_teacher)
    db.refresh(db_profile)
    return db_teacher


@router.post("/students", response_model=StudentResponse)
def create_student(student: StudentModel, db: Session = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.post("/courses", response_model=CourseResponse)
def create_course(course: CourseModel, db: Session = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.post("/enrollments", response_model=EnrollmentResponse)
def create_enrollment(enrollment: EnrollmentModel, db: Session = Depends(get_db)):

    db_student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Bachha nhi h")

    db_course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course nhi h")

    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


# get apis


@router.get("/lazy/teachers/{teacher_id}", response_model=GetTeacherResponse)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).options(
        joinedload(Teacher.department),
        joinedload(Teacher.teacher_profile)
    ).filter(Teacher.id == teacher_id).first()

    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher nhi h class me")

    return {
        "name": db_teacher.name,
        "department": db_teacher.department.name if db_teacher.department else None,
        "profile": db_teacher.teacher_profile
    }


@router.get("/lazy/students/{student_id}",response_model=GetStudentResponse)
def get_student(student_id:int, db:Session=Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    return {
        "name": student.name,
        "courses": [{"title":c.course.title, "semester":c.semester} for c in student.enrollments]
    }


@router.get("/lazy/courses/{course_id}")
def get_course(course_id:int, db:Session=Depends(get_db)):
    course=db.query(Course).filter(Course.id==course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course nhi h")
    
    return {
        "course":course.title,
        "students":[e.student.name for e in course.enrollments]
    }