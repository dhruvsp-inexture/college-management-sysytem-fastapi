import json


class TestAdmin:

    def test_assign_course_success_200(self, client, admin_token_header, faculty_token_header, add_initial_course):
        assign_course_data = {
            "course_id": 1,
            "faculty_id": 2
        }
        response = client.post('/assign-course', data=json.dumps(assign_course_data), headers=admin_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'Course Assigned successfully'
        assert response['data']['course']['name'] == 'Initial course'
        assert response['data']['course']['description'] == 'some description'
        assert response['data']['course']['course_id'] == 1
        assert response['data']['faculty']['email'] == 'faculty@gmail.com'
        assert response['data']['faculty']['first_name'] == 'Faculty'
        assert response['data']['faculty']['user_type'] == 'faculty'
        assert response['data']['faculty']['id'] == 2

    def test_assign_course_method_not_allowed_405(self, client, faculty_token_header, admin_token_header,
                                              add_initial_course):
        assign_course_data = {
            "course_id": 1,
            "faculty_id": 2
        }
        response = client.patch('/assign-course', data=json.dumps(assign_course_data), headers=admin_token_header)
        assert response.status_code == 405
        assert response.json()['detail'] == 'Method Not Allowed'

    def test_assign_course_fail_already_assigned_400(self, client, admin_token_header, faculty_token_header,
                                                  add_initial_course):
        self.test_assign_course_success_200(client, admin_token_header, faculty_token_header, add_initial_course)
        assign_course_data = {
            "course_id": 1,
            "faculty_id": 2
        }
        response = client.post('/assign-course', data=json.dumps(assign_course_data), headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Faculty with id 2 is already assigned course with id 1'

    def test_assign_course_fail_course_not_found_400(self, client, faculty_token_header, admin_token_header,
                                                     add_initial_course):
        assign_course_data = {
            "course_id": 100,
            "faculty_id": 2
        }
        response = client.post('/assign-course', data=json.dumps(assign_course_data), headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Course Not found with id 100'

    def test_assign_course_fail_faculty_not_found_400(self, client, faculty_token_header, admin_token_header,
                                                      add_initial_course):
        assign_course_data = {
            "course_id": 1,
            "faculty_id": 100
        }
        response = client.post('/assign-course', data=json.dumps(assign_course_data), headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Faculty not found with id 100'

    def test_get_all_admins_success_200(self, client, admin_token_header):
        response = client.get('/users/admin', headers=admin_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'all admin fetched successfully'
        assert len(response['data']) == 1
        assert response['data'][0]['email'] == 'admin@gmail.com'
        assert response['data'][0]['first_name'] == 'Dhruv'
        assert response['data'][0]['user_type'] == 'admin'

    def test_get_all_faculties_success_200(self, client, admin_token_header, faculty_token_header):
        response = client.get('/users/faculty', headers=admin_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'all faculty fetched successfully'
        assert len(response['data']) == 1
        assert response['data'][0]['email'] == 'faculty@gmail.com'
        assert response['data'][0]['first_name'] == 'Faculty'
        assert response['data'][0]['user_type'] == 'faculty'

    def test_get_all_students_success_200(self, client, admin_token_header, student_token_header):
        response = client.get('/users/student', headers=admin_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'all student fetched successfully'
        assert len(response['data']) == 1
        assert response['data'][0]['email'] == 'student@gmail.com'
        assert response['data'][0]['first_name'] == 'Student'
        assert response['data'][0]['user_type'] == 'student'

    def test_get_users_from_type_fail_400(self, client, admin_token_header, student_token_header):
        response = client.get('/users/notuser', headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'No such users found'

    def test_unassign_course_success_200(self, client, admin_token_header, faculty_token_header, add_initial_course):
        self.test_assign_course_success_200(client, admin_token_header, faculty_token_header, add_initial_course)
        unassign_course_data = {
            "course_id": 1,
            "faculty_id": 2
        }
        response = client.post('/unassign-course', data=json.dumps(unassign_course_data), headers=admin_token_header)
        assert response.status_code == 200
        assert response.json()['message'] == 'Course Unassigned Successfully'

    def test_unassign_course_fail_not_found_400(self, client, admin_token_header):
        unassign_course_data = {
            "course_id": 100,
            "faculty_id": 200
        }
        response = client.post('/unassign-course', data=json.dumps(unassign_course_data), headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'No faculty found assigned with this course'

    def test_get_all_assigned_courses_200(self, client, admin_token_header, faculty_token_header, add_initial_course):
        self.test_assign_course_success_200(client, admin_token_header, faculty_token_header, add_initial_course)
        response = client.get('/assign-course', headers=admin_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'Assigned Courses fetched successfully'
        assert response['data'][0]['course_data']['name'] == 'Initial course'
        assert response['data'][0]['course_data']['description'] == 'some description'
        assert response['data'][0]['faculty_data']['first_name'] == 'Faculty'
        assert response['data'][0]['faculty_data']['email'] == 'faculty@gmail.com'
        assert response['data'][0]['faculty_data']['user_type'] == 'faculty'

