from fastapi import status
from fastapi.encoders import jsonable_encoder
from clg_man.Student.models import StudentCourseMapping
from clg_man.courses.models import Course
from clg_man.language import Response


class StudentServices:

    @staticmethod
    def enroll_course(request, db, authorize):
        student_id = authorize.get_jwt_subject()
        course_id = request.dict().get("course_id")
        if not Course.get_course_by_id(db, course_id):
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=f"Course Not found with id {course_id}"
                            ).send_error_response()
        if db.query(StudentCourseMapping).filter_by(course_id=course_id, student_id=student_id).first():
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=f"You have already enrolled in this course with id {course_id}"
                            ).send_error_response()

        enrolled_data = StudentCourseMapping(student_id=student_id, course_id=course_id)
        db.add(enrolled_data)
        db.commit()
        return Response(status_code=status.HTTP_201_CREATED,
                        message="Course enrolled successfully",
                        data=jsonable_encoder(enrolled_data.course_mapping_student)).send_success_response()

    @staticmethod
    def drop_course(request, db, authorize):
        student_id = authorize.get_jwt_subject()
        course_id = request.dict().get("course_id")
        enrolled_course_data = db.query(StudentCourseMapping).filter_by(course_id=course_id,
                                                                        student_id=student_id).first()
        if not enrolled_course_data:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=f"You have not enrolled in course with id {course_id}"
                            ).send_error_response()
        db.delete(enrolled_course_data)
        db.commit()
        return Response(status_code=status.HTTP_200_OK,
                        message="Course dropped successfully"
                        ).send_success_response()

    @staticmethod
    def get_all_enrolled_courses(db, authorize):
        student_id = authorize.get_jwt_subject()
        enrolled_courses = db.query(StudentCourseMapping).filter_by(student_id=student_id).all()
        return Response(status_code=status.HTTP_200_OK,
                        message="Enrolled Courses Fetched successfully",
                        data=[jsonable_encoder(ec.course_mapping_student) for ec in enrolled_courses]
                        ).send_success_response()
