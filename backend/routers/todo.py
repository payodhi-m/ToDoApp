from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import get_db
from dependencies import get_current_user

#router = APIRouter(prefix="/todos", tags=["todos"],)

router = APIRouter()

@router.get("/todos", response_model=List[schemas.TodoBase])
def read_todos(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
        return crud.get_todos_for_user(db=db, user_id=current_user.id)

@router.post("/todos", response_model=schemas.TodoBase)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
        return crud.create_todo(db=db, todo=todo, user_id=current_user.id)

@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db), current_user: models.User= Depends(get_current_user)):
        return crud.update_todo(db=db, todo_id = todo_id, todo=todo, user_id=current_user.id)

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
        crud.delete_todo(db=db, todo_id = todo_id, user_id = current_user.id)
        return {"message": "Todo item deleted"}

