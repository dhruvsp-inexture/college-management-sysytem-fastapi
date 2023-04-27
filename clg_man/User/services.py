from clg_man.User.models import User
from sqlalchemy.exc import IntegrityError


class UserServices:
    @staticmethod
    def create(request, db_session):

        is_saved, data_or_error = User.save(db_session, request.dict())
        if is_saved is False:
            return {"error": data_or_error}
        return {"success": "successfully registered"}