import json
import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from clg_man import create_app
from database import Base, get_db
from sqlalchemy.engine.base import Engine
from clg_man import error_exception_handler
from clg_man.User import models
from clg_man.courses import models
from clg_man.Admin import models
from clg_man.Student import models

load_dotenv()
# test_engine: Engine = create_engine(os.environ.get('TESTING_DATABASE_URI'))
# # test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(bind=test_engine)
# Base.metadata.create_all(bind=test_engine)
#
#
# # Define a fixture to create a new database session for each test
# @pytest.fixture
# def db():
#     # Start a new database transaction for each test
#     conn = test_engine.connect()
#     trans = conn.begin()
#
#     # Create a new session bound to the transaction
#     session = TestingSessionLocal(bind=conn, autoflush=False)
#
#     # Make the session available to the test
#     yield session
#
#     # Roll back the transaction to clean up the database
#     session.close()
#     trans.rollback()
#     conn.close()
#
#
# # Define a fixture to create the test client for the application
# @pytest.fixture
# def client(db):
#
#     app = create_app()
#     app.dependency_overrides[get_db] = lambda: db
#     return TestClient(app)
#
#
# @pytest.fixture
# def admin_token_header(client, db):
#     # response = client.post('/register', data=json.dumps(data))
#     data = {
#         "email": "admin@gmail.com",
#         "password": "password"
#     }
#     response = client.post("/login", data=json.dumps(data))
#
#     access_token = response.json()['data']["access_token"]
#
#     return f"Bearer {access_token}"


"""New version of conftest.py"""
load_dotenv()
engine: Engine = create_engine(os.getenv('TEST_DATABASE_SQL_URI'))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def start_application():
    return create_app()


@pytest.fixture(scope="function")
def app():
    Base.metadata.create_all(bind=engine)
    Base.metadata.bind = engine
    TestingSessionLocal.bind = engine

    app = start_application()
    yield app
    # Base.metadata.drop_all(engine)


@pytest.fixture(scope="function", autouse=True)
def db(app):
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    yield db  # use the session in tests.
    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app, db):
    app.dependency_overrides[get_db] = lambda: db
    client = TestClient(app)
    yield client


@pytest.fixture(scope='function')
def admin_token_header(client, db):
    # response = client.post('/register', data=json.dumps(data))
    data = {
        "email": "admin@gmail.com",
        "password": "password"
    }
    response = client.post("/login", data=json.dumps(data))
    access_token = response.json()['data']["access_token"]
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture(scope='function')
def add_initial_course(client, db, admin_token_header):
    course_data = {
        "name": "Initial course",
        "description": "some description",
        "start_date": "2023-06-04",
        "end_date": "2023-06-05",
        "price": 100
    }
    response = client.post('/course', data=json.dumps(course_data), headers=admin_token_header)
    return response.json()
