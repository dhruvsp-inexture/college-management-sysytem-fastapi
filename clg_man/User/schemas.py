from typing import Union

from pydantic import BaseModel, EmailStr


class UserRegistrationRequestSchema(BaseModel):
    email: EmailStr
    password: str
    user_type: Union[str, None] = 'student'
    first_name: str
    last_name: Union[str, None] = None
    address: Union[str, None] = None
    phone_number: str

    class Config:
        orm_mode = True

