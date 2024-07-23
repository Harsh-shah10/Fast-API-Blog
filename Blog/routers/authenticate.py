from fastapi import FastAPI, Depends, HTTPException, Response, status, APIRouter
from hashing import HashPassword
from sqlalchemy.orm import Session

from database import get_db
import schemas, models
import create_token


router = APIRouter(
    tags=['Authentication'],
)

@router.post("/login")
def login(request: schemas.UserLogin,  db:Session=Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.email==request.username.strip()).first()
    if not user_exist:
        raise HTTPException(status_code=404, detail="Invalid username Passed !!")

    if not HashPassword.verify_password(request.password, user_exist.password):
        raise HTTPException(status_code=404, detail="Incorrect Password !!")

    access_token = create_token.create_access_token(
        data={"sub": user_exist.email}
    )

    return {"access_token": access_token, "token_type": "Bearer"}