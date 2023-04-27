import uvicorn
from clg_man import create_app
from clg_man.User import models
from clg_man.database import engine

app = create_app()
models.Base.metadata.create_all(bind=engine)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
