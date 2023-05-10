import json


class TestCourse:
    def test_add_course_success_200(self, client, db, admin_token_header):
        course_data = {
            "name": "Computer Science",
            "description": "some description",
            "start_date": "2023-06-04",
            "end_date": "2023-06-05",
            "price": 100
        }
        response = client.post('/course', data=json.dumps(course_data), headers=admin_token_header)
        response = response.json()
        assert response['status_code'] == 201
        assert response['message'] == 'Course Created successfully'
        assert response['data'] == course_data

    # def test_add_course_fail_course_exists(self, client, db, admin_token_header, add_initial_course):
    #     course_data = {
    #         "name": "Initial course",
    #         "description": "some description",
    #         "start_date": "2023-06-04",
    #         "end_date": "2023-06-05",
    #         "price": 100
    #     }
    #     response = client.post('/course', data=json.dumps(course_data), headers=admin_token_header)

    def test_add_course_fields_missing(self, client, db, admin_token_header):
        course_data = {
            "name": "Computer Science"
        }
        response = client.post('/course', data=json.dumps(course_data), headers=admin_token_header)
        assert response.status_code == 422
        assert response.json()['detail'][0]['loc'][1] == 'description'
        assert response.json()['detail'][1]['loc'][1] == 'start_date'
        assert response.json()['detail'][2]['loc'][1] == 'end_date'
        assert response.json()['detail'][3]['loc'][1] == 'price'
        assert response.json()['detail'][0]['msg'] == 'field required'

    def test_add_course_invalid_start_date(self, client, db, admin_token_header):
        course_data = {
            "name": "Computer Science",
            "description": "some description",
            "start_date": "2000-06-04",
            "end_date": "2023-06-05",
            "price": 100
        }
        response = client.post('/course', data=json.dumps(course_data), headers=admin_token_header)
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == "start date should not be before today's date"

    def test_add_course_invalid_end_date(self, client, db, admin_token_header):
        course_data = {
            "name": "Computer Science",
            "description": "some description",
            "start_date": "2023-06-04",
            "end_date": "2000-06-05",
            "price": 100
        }
        response = client.post('/course', data=json.dumps(course_data), headers=admin_token_header)
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == "end date should be after start date"

    def test_add_course_invalid_price(self, client, db, admin_token_header):
        course_data = {
            "name": "Computer Science",
            "description": "some description",
            "start_date": "2023-06-04",
            "end_date": "2023-06-05",
            "price": -99
        }
        response = client.post('/course', data=json.dumps(course_data), headers=admin_token_header)
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == "Price can not be less than 0"

    def test_get_course(self, client, db, admin_token_header, add_initial_course):
        response = client.get('/course/1', headers=admin_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'Initial course successfully fetched'
        assert response['data']['name'] == 'Initial course'
        assert response['data']['description'] == 'some description'
        assert response['data']['start_date'] == '2023-06-04'
        assert response['data']['end_date'] == '2023-06-05'
        assert response['data']['price'] == 100.0

    def test_get_course_not_found_400(self, client, db, admin_token_header):
        response = client.get('/course/100', headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Course not found with id 100'

    def test_get_all_courses(self, client, db, admin_token_header, add_initial_course):
        self.test_add_course_success_200(client, db, admin_token_header)
        response = client.get('/course', headers=admin_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == 'All courses successfully fetched'
        assert response['data'][0]['name'] == 'Initial course'
        assert response['data'][0]['description'] == 'some description'
        assert response['data'][1]['name'] == 'Computer Science'
        assert response['data'][1]['description'] == 'some description'

    def test_update_course_success_200(self, client, db, admin_token_header, add_initial_course):
        update_course_name = {"name": "updated course name"}
        response = client.patch('/course/1', data=json.dumps(update_course_name), headers=admin_token_header)
        assert response.status_code == 200
        assert response.json()['message'] == 'Course updated successfully'
        assert response.json()['data']['name'] == update_course_name['name']

    def test_update_course_invalid_start_date(self, client, db, admin_token_header, add_initial_course):
        update_course_name = {"start_date": "2025-06-04"}
        response = client.patch('/course/1', data=json.dumps(update_course_name), headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'start_date must be before end_date'

    def test_update_course_invalid_end_date(self, client, db, admin_token_header, add_initial_course):
        update_course_name = {"end_date": "2000-06-04"}
        response = client.patch('/course/1', data=json.dumps(update_course_name), headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'end_date must be after start_date'

    def test_delete_course_success_200(self, client, db, admin_token_header, add_initial_course):
        response = client.delete('/course/1', headers=admin_token_header)
        assert response.status_code == 200
        assert response.json()['message'] == 'Initial course deleted successfully'

    def test_delete_course_not_found(self, client, db, admin_token_header, add_initial_course):
        response = client.delete('/course/100', headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'No course found with id 100'
