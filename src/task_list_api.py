from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from .database import get_db
from sqlalchemy.orm import Session
from . import task_list, crud

class ToDoCreate(BaseModel):
     task: str = ""

class TaskResponse(BaseModel):
     id: int
     task: str
     isFinished: bool

app = FastAPI()

@app.get("/tasks")
def get_tasks(db : Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.get("/tasks/{taskId}")
def get_task_by_id(taskId: int):
    currentTasks = task_list.load_tasks()
    task = task_list.find_task(currentTasks, taskId)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id of {taskId} not found!")
    return task

@app.post("/tasks")
def add_task(toDo: ToDoCreate):
     currentTasks = task_list.load_tasks()
     currentId = task_list.load_id_counter()
     newIdCounter = task_list.add_task(currentTasks,[toDo.task],currentId)

     task_list.save_tasks(currentTasks)
     task_list.save_id_counter(newIdCounter)

     return TaskResponse(id=currentId, task=toDo.task, isFinished=False)


@app.put("/tasks/{taskId}",response_model=TaskResponse)
def update_task(taskId: str, toDo: ToDoCreate):
     command :list[str] = []
     command.append(taskId)
     command.append(toDo.task)
     currentTasks = task_list.load_tasks()
     updatedTask = task_list.update_task(currentTasks,command)
     if updatedTask:
          task_list.save_tasks(currentTasks)
          return updatedTask
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Task with id: {taskId} not found")

@app.delete("/tasks/{taskId}")
def delete_task(taskId: str):
     currentTasks = task_list.load_tasks()
     removedTask = task_list.delete_task(currentTasks,[taskId])
     if removedTask:
          task_list.save_tasks(currentTasks)
          return {"message": "successfully deleted the task!"}
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Task with id: {taskId} not found")

@app.patch("/tasks/{taskid}", response_model=TaskResponse)
def finish_task(taskId: str):
     currentTasks = task_list.load_tasks()
     finishedTask= task_list.finish_task(currentTasks,[taskId])
     if finishedTask:
          task_list.save_tasks(currentTasks)
          return finishedTask
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Task with id: {taskId} not found")
      