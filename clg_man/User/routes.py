from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from clg_man.User import schemas
from clg_man.User.services import UserServices
from clg_man.permissions import permission
from database import get_db

user_router = APIRouter(
    tags=['users']
)


@permission(permissions_to=['admin'])
def create_user(request: schemas.UserRegistrationRequestSchema, db: Session = Depends(get_db),
                authorize: AuthJWT = Depends()):
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


@permission(permissions_to=['admin'])
def get_all_users(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    return UserServices.get_all_users(db)


def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(get_db)):
    return UserServices.forgot_password(request, db)


def reset_password(request: schemas.ResetPassword, db: Session = Depends(get_db)):
    return UserServices.reset_password(request, db)


user_router.add_api_route("/login", login_user, methods=['POST'])
user_router.add_api_route("/register", create_user, methods=["POST"])
user_router.add_api_route("/profile", get_user, methods=["GET"], response_model=schemas.UserProfileSchema)
user_router.add_api_route("/user", update_user, methods=["PATCH"])
user_router.add_api_route("/change-password", change_password, methods=["PUT"])
user_router.add_api_route("/users", get_all_users, methods=["GET"])
user_router.add_api_route("/forgot-password", forgot_password, methods=['POST'])
user_router.add_api_route("/reset-password", reset_password, methods=['PUT'])
