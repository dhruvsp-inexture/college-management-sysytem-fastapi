from datetime import date
from fastapi import status
from fastapi.encoders import jsonable_encoder
from clg_man.Admin.models import FacultyCourseMapping
from clg_man.Student.models import StudentCourseMapping
from clg_man.language import Response


class FacultyServices:

    @staticmethod
    def get_faculty_assigned_courses(db, authorize):
        faculty_id = authorize.get_jwt_subject()
        faculty_assigned_courses = db.query(FacultyCourseMapping).filter_by(faculty_id=faculty_id).all()
        data = []
        for course in faculty_assigned_courses:
            data_dict = jsonable_encoder(course.course_mapping)
            data_dict['enrolled_students'] = []
            for student in course.course_mapping.students:
                student_data = jsonable_encoder(student.student_mapping)
                student_data['grade'] = student.grade
                data_dict['enrolled_students'].append(student_data)
            data.append(data_dict)
        return Response(status_code=status.HTTP_200_OK,
                        message="Assigned courses and its enrolled students fetched successfully",
                        data=data
                        ).send_success_response()

    @staticmethod
    def grade_students(request, db, authorize):
        course_id = request.dict().get('course_id')
        student_id = request.dict().get('student_id')
        faculty_id = authorize.get_jwt_subject()
        student_data = db.query(StudentCourseMapping).join(FacultyCourseMapping,
                                                           StudentCourseMapping.course_id == FacultyCourseMapping.course_id).filter(
            FacultyCourseMapping.faculty_id == faculty_id, FacultyCourseMapping.course_id == course_id,
            StudentCourseMapping.student_id == student_id).first()
        if not student_data:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message="Student with this enrolled course not found"
                            ).send_error_response()
        course_end_date = student_data.course_mapping_student.end_date
        if course_end_date > date.today():
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message=f"Course has not ended yet. It will end on {course_end_date}."
                            ).send_error_response()
        student_data.grade = request.dict().get('grade')
        db.commit()

        return Response(status_code=status.HTTP_200_OK,
                        message="Grades added successfully",
                        data={"course": student_data.course_mapping_student, "student": student_data.student_mapping,
                              "grade": student_data.grade}
                        ).send_success_response()
