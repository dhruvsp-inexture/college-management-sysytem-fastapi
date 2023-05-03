from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from clg_man.Admin.services import AdminServices
from database import get_db
from clg_man.Admin import schemas

admin_router = APIRouter(
    tags=['admin']
)


def assign_course(request: schemas.AssignCourseRequestSchema, db: Session = Depends(get_db),
                  authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return AdminServices.assign_course(request, db)


def get_all_students(usertype: str, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return AdminServices.get_users_from_type(usertype, db)


def unassign_course(request: schemas.AssignCourseRequestSchema, db: Session = Depends(get_db),
                    authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return AdminServices.unassign_course(request, db)


def get_all_assigned_courses(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return AdminServices.show_all_assigned_courses(db)


admin_router.add_api_route("/assign-course", assign_course, methods=['POST'])
admin_router.add_api_route("/users/{usertype}", get_all_students, methods=['GET'])
admin_router.add_api_route("/unassign-course", unassign_course, methods=['DELETE'])
admin_router.add_api_route("/assign-course", get_all_assigned_courses, methods=['GET'])
