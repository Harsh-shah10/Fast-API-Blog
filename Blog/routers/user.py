from fastapi import FastAPI, Depends, HTTPException, Response, status, APIRouter
from typing import Optional
import uvicorn
from hashing import HashPassword
from typing import List
from sqlalchemy.orm import Session

from database import get_db
import schemas 
import models 

router = APIRouter()


# Creating a new user
@router.post('/user', tags=['users'])
def create_user(request: schemas.User,  db:Session=Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.email==request.email.strip()).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exists !!")

    # hashed_password = pwd_context.hash(request.password)
    hashed_password = HashPassword.brcypt(request.password)

    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user)
    return {'message': f'User created successfully with email : {request.email} !!'}


# Fetching the particular user
@router.get("/user/{id}/", status_code=200, response_model=schemas.ShowUser, tags=['users'])
def show_user(id : int, response: Response, db:Session=Depends(get_db)):
    data = db.query(models.User).filter(models.User.id==id).first()
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail=f"User not found with id - {id}")


# Fetching all the blogs for that particluar user
@router.get("/user/blogs/{id}/", status_code=200, response_model=schemas.ShowUserBlogs, tags=['users'])
def fetch_created_blogs(id : int, response: Response, db:Session=Depends(get_db)):
    data = db.query(models.User).filter(models.User.id==id).first()
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail=f"User not found with id - {id}")
