#any fixtures I define here will be accessible to the whole package and sub packages so this is package specific
from app.database import get_db, Base
from app.main import app
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pytest
from app.oauth2 import create_access_token
from app import models

load_dotenv("/home/atharv/python/.env")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
    f"_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
#fixture scope
# function:the default scope, the fixture is destroyed at the end of the test.
# class: the fixture is destroyed during teardown of the last test in the class.
# module: the fixture is destroyed during teardown of the last test in the module.
# package: the fixture is destroyed during teardown of the last test in the package.
# sessions the fixture is destroyed   at the end of the test session.
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# client = TestClient(app)
@pytest.fixture(scope="function")
def client(session):
    #run our code before we run out test
    def override_get_db():
        try:
            yield session 
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    #run our code after the test finishes

@pytest.fixture
def test_user(client):
    user_data = {"email": "XYZ@gmail.com", "password": "12345678"}   
    res = client.post("/users/", json = user_data)
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user_other(client):
    user_data = {"email": "X_@gmail.com", "password": "12345678"}   
    res = client.post("/users/", json = user_data)
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user_other):
    session.add_all([
        models.Post(title="first title", content="first content", owner_id=test_user['id'], rating=3),
        models.Post(title="2nd title", content="2nd content", owner_id=test_user['id'], rating=4), 
        models.Post(title="3rd title", content="3rd content", owner_id=test_user_other['id'], rating=4)
    ])
    session.commit()
    posts = session.query(models.Post).all()
    return posts

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    models.Vote(post_id=test_posts[2].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
