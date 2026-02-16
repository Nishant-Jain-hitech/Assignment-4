from datetime import datetime
from pydantic import BaseModel, EmailStr


class TeacherResponse(BaseModel):
    id:int
    name: str
    email: EmailStr
    department_id:int
    qualification: str
    experience_years: int


class DepartmentResponse(BaseModel):
    id:int
    name: str


class StudentResponse(BaseModel):
    id:int
    name: str
    email: EmailStr


class CourseResponse(BaseModel):
    id:int
    title:str
    credits: int


class EnrollmentResponse(BaseModel):
    id:int
    student_id: int
    course_id:int
    semester:int
    enrolled_at:datetime

