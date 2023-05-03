from fastapi import status
from fastapi.encoders import jsonable_encoder
from clg_man.Admin.models import FacultyCourseMapping
from clg_man.User.models import User
from clg_man.courses.models import Course
from clg_man.language import Response


class AdminServices:

    @staticmethod
    def assign_course(request, db_session):
        course_id = request.dict().get('course_id')
        faculty_id = request.dict().get('faculty_id')
        if db_session.query(FacultyCourseMapping).filter_by(faculty_id=faculty_id, course_id=course_id).first():
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=f"Faculty with id {faculty_id} is already assigned course with id {course_id}"
                            ).send_error_response()
        course = Course.get_course_by_id(db_session, course_id)
        faculty = db_session.query(User).filter_by(id=faculty_id, user_type='faculty').first()
        if course and faculty:
            assign_course_data = FacultyCourseMapping(course_id=course_id,
                                                      faculty_id=faculty_id)
            db_session.add(assign_course_data)
            db_session.commit()
            return Response(status_code=status.HTTP_201_CREATED,
                            message="Assigned course successfully",
                            data=jsonable_encoder(request.dict())).send_success_response()
        return (
            Response(status_code=status.HTTP_400_BAD_REQUEST,
                     message=f"Faculty not found with id {faculty_id}"
                     ).send_error_response()
            if course
            else Response(status_code=status.HTTP_400_BAD_REQUEST,
                          message=f"Course Not found with id {course_id}"
                          ).send_error_response()
        )

    @staticmethod
    def get_users_from_type(usertype, db_session):
        if usertype in ('admin', 'faculty', 'student'):
            users_data = db_session.query(User).filter_by(user_type=usertype).all()
            return Response(status_code=status.HTTP_200_OK,
                            message=f"all {usertype} fetched successfully",
                            data=jsonable_encoder(users_data)).send_success_response()
        return Response(status_code=status.HTTP_400_BAD_REQUEST, message="No such users found").send_error_response()
