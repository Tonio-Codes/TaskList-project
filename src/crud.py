from .models import Task
from sqlalchemy.orm import Session


#file holding the CRUD operations of the db


def get_tasks(db: Session):
    tasks = db.query(Task).all()
    return tasks

def get_task(db: Session, id:int):
    task = db.query(Task).filter_by(id=id).one_or_none()
    return task

def create_task(db: Session, to_do: str):
    task = Task(task=to_do)
    db.add(task)
    db.commit()
    return task

def finish_task(db: Session, id: int):
    task = get_task(db, id)
    if task:
        task.is_finished = True
        db.commit()
    return task
   

def delete_task(db: Session, id: int):
    task = get_task(db, id)
    if task:
        db.delete(task)
        db.commit()
    return task


def update_task(db: Session, id: int, new_task: str):
    found_task = get_task(db,id)
    if found_task:
        found_task.task = new_task
        db.commit()
    return found_task
