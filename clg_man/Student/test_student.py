import json


class TestStudent:
    def test_enroll_course_success_201(self, client, student_token_header, add_initial_course):
        enroll_course_data = {
            "course_id": 1
        }
        response = client.post('/enroll-course', data=json.dumps(enroll_course_data), headers=student_token_header)
        response = response.json()
        assert response['status_code'] == 201
        assert response['message'] == 'Course enrolled successfully'
        assert response['data']['name'] == 'Initial course'
        assert response['data']['description'] == 'some description'
        assert response['data']['course_id'] == enroll_course_data['course_id']

    def test_enroll_course_fail_already_enrolled_400(self, client, student_token_header, add_initial_course):
        self.test_enroll_course_success_201(client, student_token_header, add_initial_course)
        enroll_course_data = {
            "course_id": 1
        }
        response = client.post('/enroll-course', data=json.dumps(enroll_course_data), headers=student_token_header)
        assert response.status_code == 400
        assert response.json()[
                   'detail'] == f'You have already enrolled in this course with id {enroll_course_data["course_id"]}'

    def test_enroll_course_fail_course_not_found_400(self, client, student_token_header):
        enroll_course_data = {
            "course_id": 100
        }
        response = client.post('/enroll-course', data=json.dumps(enroll_course_data), headers=student_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == f'Course Not found with id {enroll_course_data["course_id"]}'

    def test_drop_course_success_200(self, client, student_token_header, add_initial_course):
        self.test_enroll_course_success_201(client, student_token_header, add_initial_course)
        drop_course_data = {
            "course_id": 1
        }
        response = client.post('/drop-course', data=json.dumps(drop_course_data), headers=student_token_header)
        assert response.status_code == 200
        assert response.json()['message'] == 'Course dropped successfully'

    def test_drop_course_fail_not_enrolled_400(self, client, student_token_header):
        drop_course_data = {
            "course_id": 100
        }
        response = client.post('/drop-course', data=json.dumps(drop_course_data), headers=student_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == f'You have not enrolled in course with id {drop_course_data["course_id"]}'

    def test_get_all_enrolled_courses_200(self, client, student_token_header, add_initial_course):
        self.test_enroll_course_success_201(client, student_token_header, add_initial_course)
        response = client.get('/enroll-course', headers=student_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'Enrolled Courses Fetched successfully'
        assert len(response['data']) == 1
        assert response['data'][0]['name'] == 'Initial course'
        assert response['data'][0]['description'] == 'some description'
        assert response['data'][0]['price'] == 100.0
