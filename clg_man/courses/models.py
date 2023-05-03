from typing import Any
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    price = Column(Float, nullable=False)

    faculties = relationship("FacultyCourseMapping", back_populates="course_mapping")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.price = kwargs.get("price")

    @classmethod
    def save(cls, db_session, data):
        try:
            course = cls(**data)
            db_session.add(course)
            db_session.commit()
            db_session.refresh(course)
            return True, course
        except IntegrityError as e:
            error = e.orig.diag.message_detail[4:].split("=")
            return False, error[0] + error[1]
        except SQLAlchemyError as e:
            return False, e.__str__()

    def __repr__(self) -> str:
        return self.name

    @classmethod
    def get_course_by_id(cls, db_session: Any, course_id: str):
        return db_session.query(cls).filter(cls.course_id == course_id).first()
