from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base


class StudentCourseMapping(Base):
    __tablename__ = 'student_course_mapping'

    course_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    grade = Column(String)

    course_mapping_student = relationship("Course", back_populates="students")
    student_mapping = relationship("User", back_populates="enrolled_courses")
    __table_args__ = (
        PrimaryKeyConstraint('course_id', 'student_id'),
    )
