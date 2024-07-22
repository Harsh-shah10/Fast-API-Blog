from fastapi import FastAPI, Depends, HTTPException, Response, status
from typing import Optional
import uvicorn
import models
import schemas
from hashing import HashPassword
from typing import List
from sqlalchemy.orm import Session

# Start Fast API
app = FastAPI()

# Creating the tables
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

# Importing routers
from routers.blog import router as blog_router
from routers.user import router as user_router

# Including routers 
app.include_router(blog_router)
app.include_router(user_router)


'''1
=> To run the fast api app

uvicorn main:app --reload

here, app-> refers to the name of the FastAPI() instance 
      main-> refers to the name of the python file
      
=> To get more info about the environment 
import sys
print(sys.prefix)

'''

# Test the FAST API 
@app.get("/greet/{name}/", tags=['demo'])
async def greet(name):
    return {"message": f"Welcome {name} !"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=9000)