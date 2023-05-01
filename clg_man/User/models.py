from typing import Any
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import validates
from .hashing import Hasher
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    user_type = Column(String, default='student')
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    address = Column(String)
    phone_number = Column(String)
    password = Column(String)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.email = kwargs.get("email")
        self.user_type = kwargs.get("user_type")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.address = kwargs.get("address")
        self.phone_number = kwargs.get("phone_number")
        self.password = Hasher.hash_password(kwargs.get("password"))

    @classmethod
    def save(cls, db_session, data):
        try:
            user = cls(**data)
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return True, user
        except IntegrityError as e:
            error = e.orig.diag.message_detail[4:].split("=")
            return False, error[0] + error[1]
        except SQLAlchemyError as e:
            return False, e.__str__()

    @validates('user_type')
    def validate_user_type(self, key, value):
        allowed_user_types = ['admin', 'teacher', 'student']
        if value not in allowed_user_types:
            raise ValueError(f"Invalid user choice: {value}")
        return value

    def __repr__(self) -> str:
        return f"<User {self.id}>"

    @classmethod
    def get_user_by_email(cls, db_session: Any, email: str):
        return db_session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_user_by_user_id(cls, db_session: Any, user_id: str):
        return db_session.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_user_instance(cls, db_session: Any, user_id: str):
        return db_session.query(cls).filter(cls.id == user_id)
