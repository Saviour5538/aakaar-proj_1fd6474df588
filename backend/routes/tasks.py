from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from database.models import Task
from database.config import SessionLocal

router = APIRouter(prefix="/api/tasks")

class TaskResponse(BaseModel):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_task(db: Session, user_id: UUID, title: str, description: str, completed: bool) -> TaskResponse:
    task = Task(user_id=user_id, title=title, description=description, completed=completed, created_at=datetime.utcnow())
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskResponse.from_orm(task)

async def list_tasks(db: Session, user_id: UUID) -> List[TaskResponse]:
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return [TaskResponse.from_orm(task) for task in tasks]

async def update_task(db: Session, user_id: UUID, task_id: UUID, title: str, description: str, completed: bool) -> Optional[TaskResponse]:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return None
    task.title = title
    task.description = description
    task.completed = completed
    db.commit()
    db.refresh(task)
    return TaskResponse.from_orm(task)

async def delete_task(db: Session, user_id: UUID, task_id: UUID) -> bool:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

@router.post("/", response_model=TaskResponse, operation_id="create_task", status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    title: str = Body(..., min_length=1, max_length=255, embed=True),
    description: str = Body(..., min_length=1, embed=True),
    completed: bool = Body(default=False, embed=True),
    db: Session = Depends(get_db),
    current_user: UUID = Depends(lambda: None),  # Replace with actual user retrieval logic
):
    try:
        task = await create_task(db, current_user, title, description, completed)
        return task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[TaskResponse], operation_id="list_tasks", status_code=status.HTTP_200_OK)
async def list_tasks_endpoint(
    db: Session = Depends(get_db),
    current_user: UUID = Depends(lambda: None),  # Replace with actual user retrieval logic
):
    try:
        tasks = await list_tasks(db, current_user)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{id}", response_model=TaskResponse, operation_id="update_task", status_code=status.HTTP_200_OK)
async def update_task_endpoint(
    id: UUID,
    title: str = Body(..., min_length=1, max_length=255, embed=True),
    description: str = Body(..., min_length=1, embed=True),
    completed: bool = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: UUID = Depends(lambda: None),  # Replace with actual user retrieval logic
):
    try:
        task = await update_task(db, current_user, id, title, description, completed)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{id}", operation_id="delete_task", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(lambda: None),  # Replace with actual user retrieval logic
):
    try:
        success = await delete_task(db, current_user, id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return {"detail": "Task deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))