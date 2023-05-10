import json
from starlette import status

from clg_man.User.models import User


class TestUser:

    def test_login_success_200(self, client):
        login_data = {"email": "admin@gmail.com",
                      "password": "password"}
        response = client.post('/login', data=json.dumps(login_data))
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('message') == 'login success!'

    def test_login_fail_400_invalid_username(self, client):
        login_data = {"email": "notuser@gmail.com",
                      "password": "password"}
        response = client.post('/login', data=json.dumps(login_data))
        assert response.status_code == 400
        assert response.json().get('detail') == 'invalid user name!'

    def test_login_fail_400_invalid_password(self, client):
        login_data = {"email": "admin@gmail.com",
                      "password": "notpassword"}
        response = client.post('/login', data=json.dumps(login_data))
        assert response.status_code == 400
        assert response.json().get('detail') == 'invalid password'

    def test_register_success_200(self, client, admin_token_header):
        registration_data = {
            "email": "user@gmail.com",
            "password": "user@123",
            "first_name": "Dhruv",
            "phone_number": "9876543210"
        }
        response = client.post(
            '/register',
            data=json.dumps(registration_data),
            headers=admin_token_header, content='application/json')
        assert response.status_code == 200
        assert response.json()['success'] == 'successfully registered'

    # def test_register_user_exist(self, client, admin_token_header):
    #     registration_data = {
    #         "email": "admin@gmail.com",
    #         "password": "user@123",
    #         "first_name": "Dhruv",
    #         "phone_number": "9876543210"
    #     }
    #     response = client.post(
    #         '/register',
    #         data=json.dumps(registration_data),
    #         headers=admin_token_header, content='application/json')

    def test_register_fail_invalid_email(self, client, admin_token_header):
        registration_data = {
            "email": "valid email",
            "password": "user@123",
            "first_name": "Dhruv",
            "phone_number": "9876543210"
        }
        response = client.post(
            '/register',
            data=json.dumps(registration_data),
            headers=admin_token_header, content='application/json')
        assert response.status_code == 422
        assert response.json().get('detail')[0]['msg'] == 'value is not a valid email address'

    def test_register_success_fail_invalid_user_type(self, client, admin_token_header):
        registration_data = {
            "email": "user1@gmail.com",
            "user_type": "type",
            "password": "user@123",
            "first_name": "Dhruv",
            "phone_number": "9876543210"
        }
        response = client.post(
            '/register',
            data=json.dumps(registration_data),
            headers=admin_token_header, content='application/json')
        assert response.status_code == 422
        assert response.json().get('detail')[0]['msg'] == f'Invalid user choice: {registration_data.get("user_type")}'

    def test_register_success_fail_invalid_password_format(self, client, admin_token_header):
        registration_data = {
            "email": "user1@gmail.com",
            "password": "password",
            "first_name": "Dhruv",
            "phone_number": "9876543210"
        }
        response = client.post(
            '/register',
            data=json.dumps(registration_data),
            headers=admin_token_header, content='application/json')
        assert response.status_code == 422
        assert response.json().get('detail')[0][
                   'msg'] == 'Password comprises of 8 letter which includes atleast one char, one number and one special character'

    def test_register_success_fail_invalid_password_format(self, client, admin_token_header):
        registration_data = {
            "email": "user1@gmail.com",
            "password": "user@123",
            "first_name": "Dhruv",
            "phone_number": "0123456789000"
        }
        response = client.post(
            '/register',
            data=json.dumps(registration_data),
            headers=admin_token_header, content='application/json')
        assert response.status_code == 422
        assert response.json().get('detail')[0]['msg'] == 'Invalid phone number'

    def test_register_success_fail_fields_missing(self, client, admin_token_header):
        registration_data = {
            "email": "user1@gmail.com",
            "password": "user@123",
        }
        response = client.post(
            '/register',
            data=json.dumps(registration_data),
            headers=admin_token_header, content='application/json')

        assert response.status_code == 422
        assert response.json().get('detail')[0]['msg'] == 'field required'
        assert response.json().get('detail')[1]['msg'] == 'field required'

    def test_get_user_profile(self, client, admin_token_header):
        response = client.get('/profile', headers=admin_token_header)
        response = response.json()
        assert response['message'] == 'User retrieved successfully'
        assert response['data']['email'] == 'admin@gmail.com'
        assert response['data']['user_type'] == 'admin'
        assert response['data']['first_name'] == 'Dhruv'
        assert response['data']['last_name'] is None
        assert response['data']['address'] is None
        assert response['data']['phone_number'] == '8953249609'

    def test_change_password_success(self, client, admin_token_header):
        change_password_data = {
            "current_password": "password",
            "new_password": "password",
            "confirm_new_password": "password"
        }
        response = client.put('/change-password', data=json.dumps(change_password_data), headers=admin_token_header)
        assert response.status_code == 200
        assert response.json()['message'] == 'Password changed successfully'

    def test_change_password_incorrect_password(self, client, admin_token_header):
        change_password_data = {
            "current_password": "incorrect",
            "new_password": "password",
            "confirm_new_password": "password"
        }
        response = client.put('/change-password', data=json.dumps(change_password_data), headers=admin_token_header)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Incorrect Password!'

    def test_change_password_fields_not_match(self, client, admin_token_header):
        change_password_data = {
            "current_password": "password",
            "new_password": "password1",
            "confirm_new_password": "password2"
        }
        response = client.put('/change-password', data=json.dumps(change_password_data), headers=admin_token_header)
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'passwords do not match'

    def test_update_user_profile_success(self, client, admin_token_header):
        update_user_data = {
            "first_name": "adminfirst"
        }
        response = client.patch('/user', data=json.dumps(update_user_data), headers=admin_token_header)
        assert response.status_code == 200
        assert response.json()['message'] == 'Updated successfully'

    def test_get_all_users(self, client, admin_token_header):
        self.test_register_success_200(client, admin_token_header)
        response = client.get('/users', headers=admin_token_header)
        assert response.status_code == 200
        response = response.json()
        assert response['message'] == "All users fetched successfully"
        assert len(response['data']) == 2
        assert response['data'][0]['email'] == 'admin@gmail.com'
        assert response['data'][1]['email'] == 'user@gmail.com'
