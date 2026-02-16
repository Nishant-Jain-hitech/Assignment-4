from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator, EmailStr


class TeacherModel(BaseModel):
    name: str
    email: EmailStr
    department_id: int
    qualification: str
    experience_years: int


class DepartmentModel(BaseModel):
    name: str


class StudentModel(BaseModel):
    name: str
    email: EmailStr


class CourseModel(BaseModel):
    title: str
    credits: int


class EnrollmentModel(BaseModel):
    student_id: int
    course_id: int
    semester: int
    enrolled_at: datetime

    @model_validator(mode="before")
    def set_enrolled_at(cls, values):
        values["enrolled_at"] = datetime.now()
        return values
