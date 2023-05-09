import re
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

    @validator('user_type')
    def validate_user_type(cls, value):
        allowed_user_types = ['admin', 'faculty', 'student']
        if value not in allowed_user_types:
            raise ValueError(f"Invalid user choice: {value}")
        return value

    @validator('phone_number')
    def validate_phone_number(cls, phone):
        phone_regex = r'^[6-9]\d{9}$'
        if not re.match(phone_regex, phone):
            raise ValueError("Invalid phone number")
        return phone

    @validator('password')
    def validate_password(cls, password):
        password_regex = r'^(?=.*[a-z])(?=.*[!@#$%^&*()_+=-])(?=.*[0-9]).{8,20}$'
        if not re.match(password_regex, password):
            raise ValueError(
                "Password comprises of 8 letter which includes atleast one char, one number and one special character")
        return password


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
