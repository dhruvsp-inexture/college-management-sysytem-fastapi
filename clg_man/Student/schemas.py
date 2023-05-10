from typing import Union
from pydantic import BaseModel


class DropCourseRequestSchema(BaseModel):
    course_id: int


class EnrollCourseRequestSchema(BaseModel):
    course_id: int
    payment_token: Union[str, None] = None


class PaymentRequestSchema(BaseModel):
    number: str
    exp_month: int
    exp_year: int
    cvc: str

    class Config:
        orm_mode = True
        extra = "forbid"
