import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db
from app.models import User, RoleEnum, StatusEnum

# Use a purely in-memory database for testing so it's isolated and fast
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Dependency Override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db_session():
    # Setup the DB purely for testing once
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Bootstrap Test users
    admin = User(name="Test Admin", email="admin.test@test.com", role=RoleEnum.admin, status=StatusEnum.active)
    viewer = User(name="Test Viewer", email="viewer.test@test.com", role=RoleEnum.viewer, status=StatusEnum.active)
    
    db.add(admin)
    db.add(viewer)
    db.commit()
    db.refresh(admin)
    db.refresh(viewer)
    
    yield db

    # Teardown
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db_session):
    # Initialize the test client natively without any auth blockers but using standard routing capabilities.
    with TestClient(app) as c:
        yield c
