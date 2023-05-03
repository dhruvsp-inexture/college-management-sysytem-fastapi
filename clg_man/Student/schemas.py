from pydantic import BaseModel


class EnrollCourseRequestSchema(BaseModel):
    course_id: int
