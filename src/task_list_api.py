from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, ConfigDict, Field
from .database import get_db
from sqlalchemy.orm import Session
from . import crud

class ToDoCreate(BaseModel):
     task: str = Field(default="",min_length=1)

class TaskResponse(BaseModel):
     model_config = ConfigDict(from_attributes=True)
     id: int
     task: str
     is_finished: bool

app = FastAPI()

@app.get("/tasks",response_model=list[TaskResponse])
def get_tasks(db : Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.get("/tasks/{taskId}", response_model=TaskResponse)
def get_task_by_id(taskId: int,db: Session = Depends(get_db)):
    task = crud.get_task(db,taskId)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id of {taskId} not found!")
    return task

@app.post("/tasks", response_model=TaskResponse)
def add_task(toDo: ToDoCreate, db: Session = Depends(get_db)):
     new_task = crud.create_task(db,toDo.task)
     return new_task

@app.put("/tasks/{taskId}",response_model=TaskResponse)
def update_task(taskId: int, toDo: ToDoCreate, db : Session = Depends(get_db)):
     updatedTask = crud.update_task(db,taskId,toDo.task)
     if updatedTask:
          return updatedTask
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Task with id: {taskId} not found")

@app.delete("/tasks/{taskId}")
def delete_task(taskId: int, db : Session = Depends(get_db)):
     removedTask = crud.delete_task(db,taskId)
     if removedTask:
          return {"message": "successfully deleted the task!"}
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Task with id: {taskId} not found")

@app.patch("/tasks/{taskId}", response_model=TaskResponse)
def finish_task(taskId: int, db : Session = Depends(get_db)):
     finishedTask = crud.finish_task(db, taskId)
     if finishedTask:
          return finishedTask
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Task with id: {taskId} not found")
      