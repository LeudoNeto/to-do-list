import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import tasks as schemas
from ..crud import tasks as crud
from ..dependencies import get_db
from ..utils.redis_cache import redis_cache, CACHE_TTL

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    redis_cache.delete("tasks:all")
    return crud.create_task(db=db, task=task)

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_schema = schemas.Task.model_validate(db_task)
    redis_cache.set(f"task:{task_id}", json.dumps(task_schema.model_dump()), ex=CACHE_TTL)
    redis_cache.delete("tasks:all")
    return task_schema

@router.patch("/{task_id}", response_model=schemas.Task)
def partial_update_task(task_id: int, task: schemas.TaskPartialUpdate, db: Session = Depends(get_db)):
    db_task = crud.partial_update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_schema = schemas.Task.model_validate(db_task)
    redis_cache.set(f"task:{task_id}", json.dumps(task_schema.model_dump()), ex=CACHE_TTL)
    redis_cache.delete("tasks:all")
    return task_schema

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    cached_task = redis_cache.get(f"task:{task_id}")
    if cached_task:
        return json.loads(cached_task)
    
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_schema = schemas.Task.model_validate(db_task)
    redis_cache.set(f"task:{task_id}", json.dumps(task_schema.model_dump()), ex=CACHE_TTL)
    return db_task

@router.get("/", response_model=list[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cache_key = f"tasks:all:{skip}:{limit}"
    cached_tasks = redis_cache.get(cache_key)
    if cached_tasks:
        return json.loads(cached_tasks)
    
    db_tasks = crud.get_tasks(db=db, skip=skip, limit=limit)

    task_schemas = [schemas.Task.model_validate(db_task) for db_task in db_tasks]   
    redis_cache.set(cache_key, json.dumps([task.model_dump() for task in task_schemas]), ex=CACHE_TTL)
    return task_schemas

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    redis_cache.delete(f"task:{task_id}")
    redis_cache.delete("tasks:all")
