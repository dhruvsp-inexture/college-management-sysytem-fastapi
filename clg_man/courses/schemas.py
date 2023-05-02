import datetime
from typing import Optional, List
from pydantic import BaseModel, validator


class CourseResponseBaseSchema(BaseModel):
    message: str
    status_code: int


class CourseRequestSchema(BaseModel):
    name: str
    description: str
    start_date: datetime.date
    end_date: datetime.date
    price: float

    class Config:
        orm_mode = True

    @validator('start_date')
    def validate_start_date(cls, start_date):
        if start_date < datetime.date.today():
            raise ValueError("start date should not be before today's date")
        return start_date

    @validator('end_date')
    def validate_end_date(cls, end_date, values):
        if values.get('start_date') and end_date < values.get('start_date'):
            raise ValueError("end date should be after start date")
        return end_date

    @validator('price')
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("Price can not be less than 0")
        return price


class UpdateCourseRequestSchema(CourseRequestSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    price: Optional[float] = None


class CourseResponseSchema(CourseResponseBaseSchema):
    data: CourseRequestSchema


class AllCourseResponseSchema(CourseResponseBaseSchema):
    data: List[CourseRequestSchema]
