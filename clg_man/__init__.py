from fastapi import FastAPI


def create_app():
    app = FastAPI(title="fast-api-project", description="Api Description", version="1.0.1")

    from clg_man.User.routes import user_router
    app.include_router(user_router)

    """
    Hey guyzzz
    """
    return app
