from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from clg_man.courses.services import CourseServices
from clg_man.permissions import permission
from database import get_db
from clg_man.courses import schemas

course_router = APIRouter(
    tags=['courses']
)


@permission(permissions_to=['admin'])
def create_course(request: schemas.CourseRequestSchema, db: Session = Depends(get_db),
                  authorize: AuthJWT = Depends()):
    return CourseServices.create(request, db)


def get_all_courses(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return CourseServices.get_all_courses(db)


def get_course(id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return CourseServices.get_course(id, db)


@permission(permissions_to=['admin'])
def update_course(id: int, request: schemas.UpdateCourseRequestSchema, db: Session = Depends(get_db),
                  authorize: AuthJWT = Depends()):
    return CourseServices.update_course(id, request, db)


@permission(permissions_to=['admin'])
def delete_course(id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    return CourseServices.delete_course(id, db)


course_router.add_api_route("/course/{id}", get_course, methods=['GET'], response_model=schemas.CourseResponseSchema)
course_router.add_api_route("/course/{id}", delete_course, methods=['DELETE'])
course_router.add_api_route("/course/{id}", update_course, methods=['PATCH'])
course_router.add_api_route("/course", create_course, methods=['POST'])
course_router.add_api_route("/course", get_all_courses, methods=['GET'],
                            response_model=schemas.AllCourseResponseSchema)
