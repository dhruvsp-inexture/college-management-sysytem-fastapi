import json
from unittest.mock import patch

class TestStudent:
    def get_payment_token_response(self, client, student_token_header):
        course_payment_data = {
            "number": "4242 4242 4242 4242",
            "exp_month": 12,
            "exp_year": 2035,
            "cvc": "123"
        }
        return client.post(
            "/course-payment",
            data=json.dumps(course_payment_data),
            headers=student_token_header,
        )

    # def test_get_payment_token_success(self, client, student_token_header):
    #     response = self.get_payment_token_response(client, student_token_header)
    #
    #     assert response.status_code == 200
    #     assert response.json()['message'] == 'Use this token for course payment'
    #     assert response.json()['data']['token']

    # def test_enroll_course_success_201(self, client, student_token_header, add_initial_course):
    #     payment_token = self.get_payment_token_response(client, student_token_header).json()['data']['token']
    #     enroll_course_data = {
    #         "course_id": 1,
    #         'payment_token': payment_token
    #     }
    #     response = client.post('/enroll-course', data=json.dumps(enroll_course_data), headers=student_token_header)
    #     response = response.json()
    #     assert response['status_code'] == 201
    #     assert response['message'] == 'Course enrolled successfully'
    #     assert response['data']['name'] == 'Initial course'
    #     assert response['data']['description'] == 'some description'
    #     assert response['data']['course_id'] == enroll_course_data['course_id']

    def test_get_payment_token_success(self, client, student_token_header):
        with patch('stripe.Token.create') as mock_create_token:
            mock_create_token.return_value = {'id': 'mock_token'}
            response = self.get_payment_token_response(client, student_token_header)
        assert response.status_code == 200
        assert response.json()['message'] == 'Use this token for course payment'
        assert response.json()['data']['token'] == 'mock_token'

    def test_enroll_course_success_201(self, client, student_token_header, add_initial_course):
        enroll_course_data = {
            "course_id": 1,
            'payment_token': 'mock_token'
        }

        with patch('stripe.PaymentIntent.create') as mock_create_payment:
            mock_create_payment.return_value = {'status': 'succeeded'}
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
