import datetime
import uuid

from clg_man.User import utils
from clg_man.User.hashing import Hasher
from clg_man.User.jwt_authentication import Token
from clg_man.User.models import User, ResetCode
from fastapi_jwt_auth import AuthJWT
from fastapi import status
from clg_man.language import Response
from fastapi.encoders import jsonable_encoder


class UserServices:
    @staticmethod
    def create(request, db_session):
        is_saved, data_or_error = User.save(db_session, request.dict())
        if is_saved is False:
            return {"error": data_or_error}
        return {"success": "successfully registered"}

    @staticmethod
    def login(request, db_session, authorize: AuthJWT):
        """
           From this request get the required params data.
           :return: Json formed response
        """
        user_email = request.email
        password = request.password
        user = User.get_user_by_email(db_session, user_email)
        if (user_email == 'admin@gmail.com') and not user:
            admin_data = {
                "email": "admin@gmail.com",
                "password": "password",
                "user_type": "admin",
                "first_name": "Dhruv",
                "phone_number": "8953249609"
            }
            # User.save(db_session, admin_data)
            user = User(email='admin@gmail.com', password='password', user_type='admin', first_name='Admin', phone_number="1234567890")

        if user is None:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message="invalid user name!").send_error_response()
        if Hasher.verify_password(password, user.password):
            tokens = Token(sub=user.id, authorize=authorize).get_tokens()
            data = jsonable_encoder(user)
            data.update(tokens)
            # return Response(status_code=status.HTTP_200_OK,
            #                 message="login success!", data=data).send_success_response()
            return Response(status_code=status.HTTP_200_OK,
                            message="login success!", data=tokens).send_success_response()
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        message="invalid password").send_error_response()

    @staticmethod
    def get_user(db_session, authorize):
        """
           From this request get the required params data.
           :return: Json formed response
        """
        user_id = authorize.get_jwt_subject()
        if user := User.get_user_by_user_id(db_session, user_id):
            return Response(status_code=status.HTTP_200_OK,
                            message="User retrieved successfully", data=jsonable_encoder(user)).send_success_response()
        return Response(status_code=status.HTTP_401_UNAUTHORIZED,
                        message='invalid token').send_error_response()

    @staticmethod
    def update_user_profile(request, db_session, authorize):
        user_id = authorize.get_jwt_subject()
        user = User.get_user_instance(db_session, user_id)
        user_data = request.dict(exclude_unset=True)
        user.update(user_data)
        db_session.commit()
        return Response(status_code=status.HTTP_200_OK,
                        message="Updated successfully").send_success_response()

    @staticmethod
    def user_change_password(request, db_session, authorize):
        user_id = authorize.get_jwt_subject()
        user = User.get_user_instance(db_session, user_id)
        if Hasher.verify_password(dict(request).get('current_password'), user.first().password):
            hashed_password = Hasher.hash_password(dict(request).get('new_password'))
            # user.update({'password': hashed_password})
            user.first().password = hashed_password
            db_session.commit()
            return Response(status_code=status.HTTP_200_OK,
                            message="Password changed successfully").send_success_response()
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message="Incorrect Password!").send_error_response()

    @staticmethod
    def get_all_users(db_session):
        all_users = db_session.query(User).all()
        return Response(status_code=status.HTTP_200_OK,
                        message="All users fetched successfully", data=all_users).send_success_response()

    @staticmethod
    def forgot_password(request, db):
        user = User.get_user_by_email(db, request.email)
        existing_user = db.query(ResetCode).filter(ResetCode.email == request.email).first()
        if not user:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message="User not found").send_error_response()

        reset_code = str(uuid.uuid1())

        if existing_user:
            existing_user.reset_code = reset_code
            existing_user.generated_at = datetime.datetime.now()
            db.commit()

        else:
            new_code = ResetCode(email=request.email, reset_code=reset_code, generated_at=datetime.datetime.now())
            db.add(new_code)
            db.commit()
            db.refresh(new_code)

        subject, recipient, message = utils.forgot_password_format(request.email, reset_code)

        """Sending Email to User"""
        utils.send_email(subject, recipient, message)
        return Response(status_code=status.HTTP_200_OK,
                        message="We have send an Email, to reset your Password.").send_success_response()

    @staticmethod
    def reset_password(request, db):

        reset_token = request.dict().get('reset_token')
        user = db.query(ResetCode).filter(ResetCode.reset_code == reset_token).first()
        if not user:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            message="Incorrect Token").send_error_response()

        email = getattr(user, 'email')

        check_user = User.get_user_by_email(db, email)
        check_user.password = Hasher.hash_password(request.password)

        delete_token = db.query(ResetCode).filter(ResetCode.email == email).first()
        db.delete(delete_token)

        db.commit()

        return Response(status_code=status.HTTP_200_OK,
                        message="Your Password has been Successfully Reset.").send_success_response()
