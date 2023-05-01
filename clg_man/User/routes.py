from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from clg_man.User import schemas
from clg_man.User.services import UserServices
from database import get_db

user_router = APIRouter(
    tags=['users']
)


def create_user(request: schemas.UserRegistrationRequestSchema, db: Session = Depends(get_db),
                authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return UserServices.create(request, db)


def login_user(request: schemas.UserLoginSchema, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    return UserServices.login(request, db, authorize)


def get_user(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return UserServices.get_user(db, authorize)


def update_user(request: schemas.UserProfileUpdateRequestSchema, db: Session = Depends(get_db),
                authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return UserServices.update_user_profile(request, db, authorize)


def change_password(request: schemas.UserPasswordChangeRequestSchema, db: Session = Depends(get_db),
                    authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return UserServices.user_change_password(request, db, authorize)


user_router.add_api_route("/login", login_user, methods=['POST'])
user_router.add_api_route("/register", create_user, methods=["POST"])
user_router.add_api_route("/user", get_user, methods=["GET"], response_model=schemas.UserProfileSchema)
user_router.add_api_route("/user", update_user, methods=["PATCH"])
user_router.add_api_route("/change-password", change_password, methods=["PUT"])
