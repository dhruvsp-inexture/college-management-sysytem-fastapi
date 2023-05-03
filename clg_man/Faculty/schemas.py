from typing import List, Union
from pydantic import BaseModel, validator
from clg_man.User.schemas import UserResponseSchema
from clg_man.courses.schemas import CourseSchema


class FacultyBaseSchema(BaseModel):
    message: str
    status_code: int


class AssignedCourseUserResponseSchema(UserResponseSchema):
    grade_in_this_course: Union[str, None] = None


class AssignedCoursesSchema(CourseSchema):
    enrolled_students: List[AssignedCourseUserResponseSchema]


class FacultyAssignedCoursesResponseSchema(FacultyBaseSchema):
    data: List[AssignedCoursesSchema]


class FacultyGradeStudentsRequestSchema(BaseModel):
    course_id: int
    student_id: int
    grade: str

    @validator('grade')
    def validate_grade(cls, grade):
        grade_list = ["A", "B", "C", "D", "E", "F"]
        if grade not in grade_list:
            raise ValueError(f'Grades should be from {grade_list}')
        return grade
