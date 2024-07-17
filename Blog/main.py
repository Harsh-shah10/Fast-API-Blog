from fastapi import FastAPI, Depends, HTTPException, Response, status
from typing import Optional
import uvicorn
import models
import schemas

from sqlalchemy.orm import Session


# Creating the tables
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

'''
=> To run the fast api app

uvicorn main:app --reload

here, app-> refers to the name of the FastAPI() instance 
      main-> refers to the name of the python file
      
=> To get more info about the environment 
import sys
print(sys.prefix)

'''

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()
        

@app.get("/test/")
async def test():
    return {"message": "I am ON !"}


@app.get("/greet/{name}/")
async def greet(name):
    return {"message": f"Welcome {name} !"}


# @app.get("/blog/")
# def fetch_blogs(limit : int = 10, published: bool = True, sort:Optional[str] = None):
#     # Fetch only 10 blogs -> also setting default value
#     if published:
#         return {'message': f'fetched {limit} -> Published blogs from DB'}
#     else:
#         return {'message': f'fetched {limit} -> blogs from DB'}
       
  
       
@app.get("/blog/{id}/comments/")
def comments(id : int, limit : int = 10):
    # Fetching 10 comments by default
    return {'message': {'1', '2'}, 'limit':limit, 'id':id}
 
 
@app.get("/blog/unpublish/")
def unpublish_blog():
    return {"message": "all blogs unpublished successfully !"}


# Query Params | items/?skip=111&limit=222
@app.get("/items/")
def fetch_items(skip: int = 0, limit: int = 10):
    return {"message": {"skip": skip, "limit": limit}}
  

# Creating a new blog
@app.post('/blog', status_code=201)
def create_blog(request: schemas.Blog,  db:Session=Depends(get_db)):
    blog_exist = db.query(models.Blog).filter(models.Blog.title==request.title.strip()).first()
    if blog_exist:
        raise HTTPException(status_code=400, detail="Blog already exists !!")

    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    
    db.refresh(new_blog)
    return {'message': f'Blog created successfully with title : {request.title} !!'}


# Fetching all the blogs
@app.get("/blog/", status_code=200)
def fetch_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {"message": "Blogs Retrieve Success !", "data":blogs}
       
       
# Fetching the particular blog
@app.get("/blog/{id}/", status_code=200)
def show_blog(id : int, response: Response, db:Session=Depends(get_db)):
    data = db.query(models.Blog).filter(models.Blog.id==id).first()
    if data:
        return {"message": "Data retrieved Success", "data": data}
    else:
        response.status_code = 404
        return {"message": "Data not found", "data": []}

# Destroy the particular blog
@app.get("/blog/{id}/", status_code=200)
def destroy(id : int, response: Response, db:Session=Depends(get_db)):
    data = db.query(models.Blog).filter(models.Blog.id==id).first()
    if data:
        data.delete()
        return {"message": "Data destroy Success"}
    else:
        response.status_code = 404
        return {"message": "Data not found"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=9000)