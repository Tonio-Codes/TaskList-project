import json
import requests
import time
#comment to test
#load in ongoing id counter to maintain unique ids for each task
def load_id_counter():
    try:
        with open('data/task_id_counter.txt','r',encoding='utf-8') as file:
            return int(file.read())
    except FileNotFoundError:
        return 1

#save the id counter to txt file once program is done running
def save_id_counter(task_id: int):
    with open('data/task_id_counter.txt','w',encoding='utf-8') as file:
        file.write(str(task_id))

#load existing list of tasks or create a new one if it DNE
def save_tasks(tasks :list[dict]):
    with open('data/task_list.json','w') as file:
        json.dump(tasks,file)

def load_tasks() -> list[dict]:
    tasks: list[dict]
    try:
        with open('data/task_list.json','r',encoding='utf-8') as file:
            print("Existing task list found!")
            print("loading in...")
            tasks = json.load(file)
    
    except (FileNotFoundError,json.JSONDecodeError, ValueError):
        tasks = [] 
    return tasks

def add_task(tasks :list[dict], task :list[str], task_id: int):
    newTask = " ".join(task).strip()
    if len(newTask) == 0:
        print("please enter a new task to add")
        return task_id

    taskDict = {
        "id": task_id,
        "task" : newTask,
        "isFinished": False
    }
    tasks.append(taskDict)
    return task_id + 1

def delete_task(tasks :list[dict], task: list[str]):
    taskId = extract_id(task)
    if taskId == -1:
        return
    
    taskToRemove = find_task(tasks, taskId)
    if taskToRemove:
        tasks.remove(taskToRemove)
    else:
        print(f"task with id {taskId} not found!")
    return
    
def update_task(tasks :list, task: list[str]):
    taskId, newTask = process_task(task)
    if taskId == -1:
        return

    taskToUpdate = find_task(tasks, taskId)
    if taskToUpdate:
        taskToUpdate["task"] = newTask
    else:
        print(f"task with id {taskId} not found!")
    return

#start on concept of finishing a task. Also update formatting of how the tasks are output to be cleaner and include emojis on the finished status
def finish_task(tasks: list, task: list[str]):
    taskId = extract_id(task)
    if taskId == -1:
        return
    taskToFinish = find_task(tasks,taskId)
    if taskToFinish:
        taskToFinish['isFinished'] = True
    else:
        print(f"task with id {taskId} not found!")
    return

#helper func to find a task 
def find_task(tasks: list, taskId: int):
    return next((elem for elem in tasks if elem['id'] == taskId),None)
    
     
def print_tasks(tasks :list):
    done :str = '\N{check mark}'
    notDone :str = '\N{cross mark}'
    if len(tasks) > 0:
        print(f"""
                Current task list
            ---------------------------""")
        for elem in tasks:
            print(f"            - ID:{elem['id']} | {elem['task']} | Done:{done if elem['isFinished'] else notDone}")
    else:
        print("your task list is currently empty")

def print_commands():
    print("""
                welcome to your personal task manager!
                ------------------------------------------
                Commands:
                - add "task"
                - delete "id"
                - finish "id"
                - update "id" "updated task"
                - 'show'
                - 'q' to quit
                - 'c' to show commands                  
            """)

def process_task(command: list):
     if len(command) < 2:
         print("please follow the correct command format")
         return - 1,""
     task = " ".join(command[1:])
     try:
        idToUpdate = int(command[0])
     except ValueError:
        print("please enter a valid task id")
        return -1, ""

     return idToUpdate, task

def extract_id(task :list[str]):
    if len(task) != 1:
        print("please enter the correct command format")
        return -1

    tempId = task[0]
    try:
        taskId = int(tempId)
    except ValueError:
        print("please enter a valid id")
        return -1
    return taskId

def task_manager():

    motivQuote = requests.get("https://motivational-spark-api.vercel.app/api/quotes/random")
    motivQuote = motivQuote.json()
    print(f"\n{motivQuote['quote']} - {motivQuote['author']}\n")
    time.sleep(2)

    task_id = load_id_counter()
    currentTasks :list = load_tasks()

    print_commands()
    while True:
        userInput :str = input("Command: ")
        command = userInput.split()

        if len(command) == 0:
            print("please enter a command")
            continue

        prefix = command[0].lower()
        if prefix == 'q':
            save_tasks(currentTasks)
            save_id_counter(task_id)
            return
        elif prefix == 'c':
            print_commands()
            continue
        elif prefix == "show":
            print_tasks(currentTasks)
            continue

        task = command[1:]
        match prefix:

            case "add":
                task_id = add_task(currentTasks, task, task_id)

            case "delete":
                delete_task(currentTasks,task)

            case "update":
                update_task(currentTasks, task)

            case "finish":
                finish_task(currentTasks, task)

            case _:
                print("Not a command!")
    
    


def main():
   task_manager()
    

if __name__ == "__main__":
    main()