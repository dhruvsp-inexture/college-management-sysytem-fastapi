from functools import wraps
from fastapi import HTTPException
from clg_man.User.models import User


def permission(permissions_to: list):
    def check_permission(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            authorize = kwargs.get('authorize')
            authorize.jwt_required()
            db = kwargs.get('db')
            current_user_id = authorize.get_jwt_subject()
            user = User.get_user_by_user_id(db, current_user_id)
            permissions_list = permissions_to or []
            if user.user_type not in permissions_list:
                raise HTTPException(status_code=403, detail='User not authorized')
            return func(*args, **kwargs)

        return wrapper

    return check_permission


# def check_permission(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print(f"testing  => {args}")
#         print(f"kwargs  => {kwargs}")
#         authorize = kwargs.get('authorize')
#         authorize.jwt_required()
#         db = kwargs.get('db')
#         current_user_id = authorize.get_jwt_subject()
#         user = User.get_user_by_user_id(db, current_user_id)
#         permissions_list = kwargs.get('permissions_to', [])
#         if user.user_type not in permissions_list:
#             raise HTTPException(status_code=403, detail='User not authorized')
#         return func(*args, **kwargs)
#     return wrapper
