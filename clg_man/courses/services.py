from fastapi.encoders import jsonable_encoder
from clg_man.language import Response
from clg_man.courses.models import Course
from fastapi import status


class CourseServices:

    @staticmethod
    def create(request, db_session):
        is_saved, data_or_error = Course.save(db_session, request.dict())
        if is_saved is False:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, message=data_or_error).send_error_response()
        return Response(status_code=status.HTTP_201_CREATED,
                        message="Course Created successfully",
                        data=jsonable_encoder(request.dict())).send_success_response()

    @staticmethod
    def get_all_courses(db_session):
        courses = db_session.query(Course).all()
        return Response(status_code=status.HTTP_200_OK,
                        message="All courses successfully fetched",
                        data=jsonable_encoder(courses)).send_success_response()

    @staticmethod
    def get_course(course_id, db_session):
        course = Course.get_course_by_id(db_session, course_id)
        return Response(status_code=status.HTTP_200_OK,
                        message=f"{course.name} successfully fetched",
                        data=jsonable_encoder(course)).send_success_response()

    @staticmethod
    def update_course(course_id, request, db_session):
        course = db_session.query(Course).filter(Course.course_id == course_id)
        course_data = request.dict(exclude_unset=True)
        if course_data.get('end_date') and course_data.get('end_date') < course.first().start_date:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="end_date must be after start_date",
            ).send_error_response()

        if course_data.get('start_date') and not course_data.get('end_date') and (
                course_data.get('start_date') > course.first().end_date):
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="start_date must be before end_date",
            ).send_error_response()

        course.update(course_data)
        db_session.commit()

        return Response(
            status_code=status.HTTP_200_OK,
            message="Course updated successfully",
            data=jsonable_encoder(course.first()),
        ).send_success_response()

    @staticmethod
    def delete_course(course_id, db_session):
        course = Course.get_course_by_id(db_session, course_id)
        if course:
            db_session.delete(course)
            db_session.commit()
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=f"{course.name} deleted successfully").send_success_response()
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=f"No course found with id {course_id}").send_success_response()
