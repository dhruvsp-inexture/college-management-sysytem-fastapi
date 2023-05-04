from typing import Union
from pydantic import BaseModel, EmailStr, validator


class UserResponseBaseSchema(BaseModel):
    message: str
    status_code: int


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


class UserResponseSchema(BaseModel):
    email: EmailStr
    user_type: Union[str, None] = 'student'
    first_name: str
    last_name: Union[str, None] = None
    address: Union[str, None] = None
    phone_number: str

    class Config:
        orm_mode = True


class UserProfileSchema(UserResponseBaseSchema):
    data: UserResponseSchema

    class Config:
        orm_mode = True


class UserProfileUpdateRequestSchema(BaseModel):
    email: Union[EmailStr, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    address: Union[str, None] = None
    phone_number: Union[str, None] = None

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserPasswordChangeRequestSchema(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

    @validator('confirm_new_password')
    def passwords_match(cls, v, values):
        if v != values.get('new_password'):
            raise ValueError('passwords do not match')
        return v

    class Config:
        orm_mode = True


class ForgotPassword(BaseModel):
    email: str


class ResetPassword(BaseModel):
    reset_token: str
    password: str
