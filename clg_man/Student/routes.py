from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from clg_man.Student import schemas
from clg_man.Student.services import StudentServices

from database import get_db

student_router = APIRouter(
    tags=['students']
)


def enroll_course(request: schemas.EnrollCourseRequestSchema, db: Session = Depends(get_db),
                  authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return StudentServices.enroll_course(request, db, authorize)


def drop_course(request: schemas.EnrollCourseRequestSchema, db: Session = Depends(get_db),
                authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return StudentServices.drop_course(request, db, authorize)


def get_all_enrolled_courses(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return StudentServices.get_all_enrolled_courses(db, authorize)


student_router.add_api_route("/enroll-course", enroll_course, methods=['POST'])
student_router.add_api_route("/drop-course", drop_course, methods=['DELETE'])
student_router.add_api_route("/enroll-course", get_all_enrolled_courses, methods=['GET'])
