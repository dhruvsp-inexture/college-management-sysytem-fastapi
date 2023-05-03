from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base


class FacultyCourseMapping(Base):
    __tablename__ = 'faculty_course_mapping'

    course_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    faculty_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    course_mapping = relationship("Course", back_populates="faculties")
    faculty_mapping = relationship("User", back_populates="assigned_courses")
    __table_args__ = (
        PrimaryKeyConstraint('course_id', 'faculty_id'),
    )
