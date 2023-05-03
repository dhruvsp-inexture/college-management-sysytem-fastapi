from pydantic import BaseModel


class AssignCourseRequestSchema(BaseModel):
    course_id: int
    faculty_id: int

    class Config:
        orm_mode = True
        extra = "forbid"
