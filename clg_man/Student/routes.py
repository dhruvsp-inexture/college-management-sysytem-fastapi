from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from clg_man.Student import schemas
from clg_man.Student.services import StudentServices
from clg_man.permissions import permission
from database import get_db

student_router = APIRouter(
    tags=['students']
)


@permission(permissions_to=['student'])
def enroll_course(request: schemas.EnrollCourseRequestSchema, db: Session = Depends(get_db),
                  authorize: AuthJWT = Depends()):
    return StudentServices.enroll_course(request, db, authorize)


@permission(permissions_to=['student'])
def drop_course(request: schemas.EnrollCourseRequestSchema, db: Session = Depends(get_db),
                authorize: AuthJWT = Depends()):
    return StudentServices.drop_course(request, db, authorize)


@permission(permissions_to=['student'])
def get_all_enrolled_courses(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    return StudentServices.get_all_enrolled_courses(db, authorize)


student_router.add_api_route("/enroll-course", enroll_course, methods=['POST'])
student_router.add_api_route("/drop-course", drop_course, methods=['POST'])
student_router.add_api_route("/enroll-course", get_all_enrolled_courses, methods=['GET'])
