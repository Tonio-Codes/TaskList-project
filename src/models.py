from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from .database import Base

#define current model for a Task

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task :Mapped[str] = mapped_column(String,nullable=False)
    is_finished :Mapped[bool] = mapped_column(Boolean,default=False)