import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.connections.db_connector import Base, get_db
from app.models.user_model import UserModel
from app.helpers.utils.password_hash import pwd_context
from app.helpers.enums.enum_config import userRoles


# Test database (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Database fixture
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# Override get_db dependency
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

#Admin User
@pytest.fixture
def admin_user(db):
    user = UserModel(
        user_name="admin",
        email="admin@test.com",
        password=pwd_context.hash("admin123"),
        role=userRoles.ADMIN,
    )
    db.add(user)
    db.commit()
    return user

# Test User
@pytest.fixture
def test_user(db):
    user = UserModel(
        user_name="user1",
        email="user1@test.com",
        password=pwd_context.hash("correctpass"),
        role=userRoles.USER,
    )
    db.add(user)
    db.commit()
    return user