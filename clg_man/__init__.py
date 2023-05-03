from fastapi import FastAPI


def create_app():
    app = FastAPI(title="fast-api-project", description="Api Description", version="1.0.1")

    from clg_man.User.routes import user_router
    from clg_man.courses.routes import course_router
    from clg_man.Admin.routes import admin_router
    from clg_man.Student.routes import student_router
    app.include_router(user_router)
    app.include_router(course_router)
    app.include_router(admin_router)
    app.include_router(student_router)
    from clg_man import error_exception_handler
    # error_exception_handler
    """
    Hey guyzzz
    """
    return app
