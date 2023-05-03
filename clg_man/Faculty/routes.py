from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from clg_man.Faculty import schemas
from clg_man.Faculty.services import FacultyServices
from database import get_db

faculty_router = APIRouter(
    tags=['faculty']
)


def get_faculty_assigned_courses(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return FacultyServices.get_faculty_assigned_courses(db, authorize)


def grade_students(request: schemas.FacultyGradeStudentsRequestSchema, db: Session = Depends(get_db),
                   authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return FacultyServices.grade_students(request, db, authorize)


faculty_router.add_api_route('/faculty-courses', get_faculty_assigned_courses, methods=['GET'],
                             response_model=schemas.FacultyAssignedCoursesResponseSchema)
faculty_router.add_api_route('/grade-student', grade_students, methods=['PUT'])
