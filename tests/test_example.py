import src.task_list as task_list
from pathlib import Path
import json

def test_add_task():
    tasks = []
    newId = task_list.add_task(tasks,["learn","python"],1)

    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["task"] == "learn python"
    assert tasks[0]["isFinished"] == False
    assert newId == 2

def test_delete_wrong_id():
    tasks = []
    assert task_list.delete_task(tasks,["4"]) == None
    assert len(tasks) == 0

def test_delete_valid_id():
    tasks = [{"id": 1, "task": "learn python", "isFinished": False},{"id": 2, "task": "do hw", "isFinished": False}]
    task_list.delete_task(tasks,["1"])

    assert len(tasks) == 1
    assert tasks[0]["id"] != 1

def test_load_id_counter():
    filePath = Path("E:/Python learning/data/task_id_counter.txt")
    idCounter = task_list.load_id_counter()

    if filePath.exists():
        savedId = int(filePath.read_text("utf-8"))
        assert idCounter == savedId
    else:
        assert idCounter == 1 

def test_save_id_counter():
    task_list.save_id_counter(4)
    filePath = Path("E:/Python learning/data/task_id_counter.txt")

    idCounter = int(filePath.read_text(encoding="utf-8"))
    assert idCounter == 4

def test_save_tasks():
    tasks = [{"id": 1, "task": "learn python", "isFinished": False},{"id": 2, "task": "do hw", "isFinished": False}]
    task_list.save_tasks(tasks)
    file_path = Path("E:/Python learning/data/task_list.json")

    assert task_list.load_tasks() == tasks


def test_load_tasks():
    tasks = task_list.load_tasks()
    filePath = Path("E:/Python learning/data/task_list.json")

    if filePath.exists():
        with open(filePath,"r") as file:
            saved_tasks = json.load(file)
        assert tasks == saved_tasks
    else:
        assert tasks == []

def test_update_task():
    tasks = [{"id": 1, "task": "learn python", "isFinished": False}]
    task_list.update_task(tasks, ["1", "go", "beach"])

    assert tasks[0]["task"] == "go beach"
    assert tasks[0]["id"] == 1
    assert tasks[0]["isFinished"] == False

def test_finish_task():
    tasks = [{"id": 1, "task": "learn python", "isFinished": False}]
    task_list.finish_task(tasks, ["1"])
    assert tasks[0]["isFinished"] == True

def test_find_task():
    tasks = [{"id": 1, "task": "learn python", "isFinished": False},{"id": 2, "task": "do hw", "isFinished": False}]
    assert task_list.find_task(tasks,1) == tasks[0]

def test_extract_id():
    command = ["5"]
    assert task_list.extract_id(command) == 5

def test_process_task():
    command = ["5", "go to store"]
    assert task_list.process_task(command) == (5, "go to store")