from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    completed: bool

class TaskPartialUpdate(BaseModel):
    completed: bool

class Task(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
