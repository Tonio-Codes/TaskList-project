from fastapi import FastAPI
from . import task_list
from pydantic import BaseModel

class Todo(BaseModel):
     task: str = ""

app = FastAPI()

@app.get("/tasks")
def get_tasks():
    return task_list.load_tasks()

@app.post("/tasks")
def add_task(toDo: Todo):
     currentTasks = task_list.load_tasks()
     currentId = task_list.load_id_counter()
     newIdCounter = task_list.add_task(currentTasks,[toDo.task],currentId)

     task_list.save_tasks(currentTasks)
     task_list.save_id_counter(newIdCounter)

     return {
          
          "id" : currentId,
          "task": toDo.task,
          "isFinished": False
     }
