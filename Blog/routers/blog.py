from fastapi import FastAPI, Depends, HTTPException, Response, status, APIRouter
from typing import Optional
import uvicorn
from hashing import HashPassword
from typing import List
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db
import schemas, models, oauth2

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)

# Creating a new blog
@router.post('/', status_code=201)
# def create_blog(request: schemas.Blog,  db:Session=Depends(get_db)):
def create_blog(request: schemas.Blog, current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],  db:Session=Depends(get_db)):
    blog_exist = db.query(models.Blog).filter(models.Blog.title==request.title.strip()).first()
    if blog_exist:
        raise HTTPException(status_code=400, detail="Blog already exists !!")

    user_exist = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user_exist:
        return {'message': f'User does not exists with ID - {request.user_id}'}

    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    
    db.refresh(new_blog)
    return {'message': f'Blog created successfully with title : {request.title} !!'}


# Fetching all the blogs
@router.get("/", response_model=List[schemas.ShowBlog], status_code=200)
# def fetch_all_blogs(db:Session=Depends(get_db)):
def fetch_all_blogs(current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
    # return {"message": "Blogs Retrieve Success !", "data":blogs}
       
       
# Fetching the particular blog
@router.get("/{id}/", status_code=200, response_model=schemas.ShowBlog)
# def show_blog(id: int, db: Session = Depends(get_db)):
def show_blog(id: int, current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], db: Session = Depends(get_db)):
    data = db.query(models.Blog).filter(models.Blog.id == id).first()
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")


# Update the particular blog
@router.put("/{id}/", status_code=201)
# def update(id : int, request: schemas.UpdateBlog, response: Response, db:Session=Depends(get_db)):
def update(id : int, request: schemas.UpdateBlog, response: Response, current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:

        if request.body:
            blog.body = request.body
        if request.title:
            blog.title = request.title

        db.commit()
        db.refresh(blog)  # Refresh the instance to reflect the updated data
        return {"message": "Blog update Success", "data": blog}
    else:
        response.status_code = 404
        return {"message": f"Blog with id {id} not found"}
    

# Destroy the particular blog
@router.delete("/{id}/", status_code=200)
# def destroy(id : int, response: Response, db:Session=Depends(get_db)):
def destroy(id : int, response: Response, current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:
        db.delete(blog)
        db.commit()
        return {"message": "Blog destroy Success"}
    else:
        response.status_code = 404
        return {"message": f"Blog with id {id} not found"}
    