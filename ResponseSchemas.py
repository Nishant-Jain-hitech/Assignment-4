from typing import List
from datetime import datetime
from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional

class TeacherProfileResponse(BaseModel):
    qualification: str
    experience_years: int

    class ConfigDict:
        from_attributes = True

class DepartmentResponse(BaseModel):
    id: int
    name: str

    class ConfigDict:
        from_attributes = True


class TeacherResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department_id: Optional[int]
    
    teacher_profile: Optional[TeacherProfileResponse]

    class ConfigDict:
        from_attributes = True


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class ConfigDict:
        from_attributes = True

class CourseResponse(BaseModel):
    id: int
    title: str
    credits: int

    class ConfigDict:
        from_attributes = True

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    semester: int
    enrolled_at: datetime

    class ConfigDict:
        from_attributes = True


class GetTeacherResponse(BaseModel):
    name: str
    department:str
    profile: Optional[TeacherProfileResponse]

    class ConfigDict:
        from_attributes = True


class GetStudentResponse(BaseModel):
    name:str
    courses:List[dict]
