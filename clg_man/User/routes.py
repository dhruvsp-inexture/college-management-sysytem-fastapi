from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from clg_man.User.schemas import UserRegistrationRequestSchema
from clg_man.User.services import UserServices
from clg_man.database import get_db

user_router = APIRouter(
    tags=['users']
)


def create_user(request: UserRegistrationRequestSchema, db: Session = Depends(get_db)):
    return UserServices.create(request, db)


user_router.add_api_route("/user", create_user, methods=["POST"])
