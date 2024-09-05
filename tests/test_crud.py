import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import tasks as models
from app.crud import tasks as crud
from app.schemas import tasks as schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        models.Base.metadata.drop_all(bind=engine)


def test_create_task(db):
    task_in = schemas.TaskCreate(title="Test Task", description="Test Description")
    task = crud.create_task(db, task_in)
    assert task.title == task_in.title
    assert task.description == task_in.description
    assert task.completed is False


def test_get_task(db):
    task_in = schemas.TaskCreate(title="Test Task", description="Test Description")
    task = crud.create_task(db, task_in)
    fetched_task = crud.get_task(db, task.id)
    assert fetched_task.id == task.id
    assert fetched_task.title == task.title
    assert fetched_task.description == task.description


def test_update_task(db):
    task_in = schemas.TaskCreate(title="Test Task", description="Test Description")
    task = crud.create_task(db, task_in)
    update_data = schemas.TaskUpdate(
        title="Updated Task", description="Updated Description", completed=True
    )
    updated_task = crud.update_task(db, task.id, update_data)
    assert updated_task.title == update_data.title
    assert updated_task.description == update_data.description
    assert updated_task.completed is True


def test_partial_update_task(db):
    task_in = schemas.TaskCreate(title="Test Task", description="Test Description")
    task = crud.create_task(db, task_in)
    update_data = schemas.TaskPartialUpdate(completed=True)
    updated_task = crud.partial_update_task(db, task.id, update_data)
    assert updated_task.completed is True


def test_delete_task(db):
    task_in = schemas.TaskCreate(title="Test Task", description="Test Description")
    task = crud.create_task(db, task_in)
    deleted_task = crud.delete_task(db, task.id)
    assert deleted_task is not None
    assert crud.get_task(db, task.id) is None
