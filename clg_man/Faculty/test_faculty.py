import json
from clg_man.Admin.test_admin import TestAdmin
from clg_man.Student.test_student import TestStudent

admin_test_cases = TestAdmin()
student_test_cases = TestStudent()


class TestFaculty:

    def test_get_faculty_assigned_courses_success_200(self, client, admin_token_header, faculty_token_header,
                                                      student_token_header, add_initial_course):
        admin_test_cases.test_assign_course_success_200(client, admin_token_header, faculty_token_header,
                                                        add_initial_course)
        student_test_cases.test_enroll_course_success_201(client, student_token_header, add_initial_course)

        response = client.get("/faculty-courses", headers=faculty_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'Assigned courses and its enrolled students fetched successfully'
        assert len(response['data']) == 1
        assert response['data'][0]['name'] == 'Initial course'
        assert response['data'][0]['description'] == 'some description'
        assert len(response['data'][0]['enrolled_students']) == 1
        assert response['data'][0]['enrolled_students'][0]['email'] == 'student@gmail.com'
        assert response['data'][0]['enrolled_students'][0]['user_type'] == 'student'
        assert response['data'][0]['enrolled_students'][0]['first_name'] == 'Student'

    def prerequisite_data_for_grading_student(self, client, admin_token_header, student_token_header):
        course_data = {
            "name": "Computer Science",
            "description": "some description",
            "start_date": "2023-05-10",
            "end_date": "2023-05-10",
            "price": 0
        }
        response1 = client.post('/course', data=json.dumps(course_data), headers=admin_token_header)

        assign_course_data = {
            "course_id": 1,
            "faculty_id": 2
        }
        response2 = client.post('/assign-course', data=json.dumps(assign_course_data), headers=admin_token_header)

        enroll_course_data = {
            "course_id": 1

        }
        response3 = client.post('/enroll-course', data=json.dumps(enroll_course_data), headers=student_token_header)

    def test_grade_student_success_200(self, client, admin_token_header, faculty_token_header, student_token_header):
        self.prerequisite_data_for_grading_student(client, admin_token_header, student_token_header)
        grade_student_data = {
            "course_id": 1,
            "student_id": 3,
            "grade": "A"
        }
        response = client.put('/grade-student', data=json.dumps(grade_student_data), headers=faculty_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'Grades added successfully'
        assert response['data']['course']['name'] == 'Computer Science'
        assert response['data']['student']['email'] == 'student@gmail.com'
        assert response['data']['grade'] == 'A'

    def test_grade_student_fail_invalid_grade(self, client, admin_token_header, faculty_token_header,
                                              student_token_header):
        self.prerequisite_data_for_grading_student(client, admin_token_header, student_token_header)
        grade_student_data = {
            "course_id": 1,
            "student_id": 3,
            "grade": "Q"
        }
        response = client.put('/grade-student', data=json.dumps(grade_student_data), headers=faculty_token_header)
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == "Grades should be from ['A', 'B', 'C', 'D', 'E', 'F']"

    def test_grade_student_fail_student_course_not_found_400(self, client, admin_token_header, faculty_token_header,
                                                             student_token_header):
        grade_student_data = {
            "course_id": 100,
            "student_id": 100,
            "grade": "A"
        }
        response = client.put('/grade-student', data=json.dumps(grade_student_data), headers=faculty_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Student with this enrolled course not found'

    def test_grade_student_fail_course_not_ended(self, client, admin_token_header, faculty_token_header,
                                                 student_token_header, add_initial_course):
        admin_test_cases.test_assign_course_success_200(client, admin_token_header, faculty_token_header,
                                                        add_initial_course)
        student_test_cases.test_enroll_course_success_201(client, student_token_header, add_initial_course)
        grade_student_data = {
            "course_id": 1,
            "student_id": 3,
            "grade": "A"
        }
        response = client.put('/grade-student', data=json.dumps(grade_student_data), headers=faculty_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Course has not ended yet. It will end on 2023-06-05.'
