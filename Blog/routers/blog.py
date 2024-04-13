from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from .. import schema, models
from ..database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List


router = APIRouter(tags=["Blogs"])
 
# insert data in db
@router.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blogs(title= request.title, body= request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# fetch data
@router.get("/blog",response_model=List[schema.Show_blog])
def get_blogs(db:Session = Depends(get_db)):
    blog = db.query(models.Blogs).all()
    return blog

# fetch single data
# response model to fetch specific data
@router.get("/blog/{id}",response_model=schema.Show_blog)
def get_blogs(id, response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
        # in one liner
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} blog is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data":f"{id} blog is not found"}
    return blog

#remove the data
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db:Session = Depends(get_db)):
    db.query(models.Blogs).filter(models.Blogs.id == id).delete(synchronize_session=False)
    db.commit()
    return "done"

#update data
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,response_model=schema.Blog)
def update_blog(id:int, request: schema.Blog,db:Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=" blog is not found")
    updated_payload = request.dict(exclude_unset=True)
    blog.update(updated_payload, synchronize_session=False)
    db.commit()
    db.refresh(blog.first())
    print(blog.first())
    return blog.first()
