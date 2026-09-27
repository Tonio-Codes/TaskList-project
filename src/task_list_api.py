from fastapi import FastAPI, HTTPException, status
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

@app.put("/tasks/{taskId}")
def update_task(taskId: str, toDo: Todo):
     command :list[str] = []
     command.append(taskId)
     command.append(toDo.task)
     currentTasks = task_list.load_tasks()
     task_list.update_task(currentTasks,command)
     task_list.save_tasks(currentTasks)
     return task_list.find_task(currentTasks, int(taskId))

@app.delete("/tasks/{taskId}")
def delete_task(taskId: str):
     currentTasks = task_list.load_tasks()
     removedTask = task_list.delete_task(currentTasks,[taskId])
     if removedTask:
          task_list.save_tasks(currentTasks)
          return {"message": "successfully deleted the task!"}
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found!")

@app.patch("/tasks/{task_id}")
def finish_task(taskId: str):
     currentTasks = task_list.load_tasks()
     finishedTask= task_list.finish_task(currentTasks,[taskId])
     if finishedTask:
          task_list.save_tasks(currentTasks)
          return finishedTask
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="task not found!")
      