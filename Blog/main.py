from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schema, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Dependency for db connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# insert data in db
@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: schema.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blogs(title= request.title, body= request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# fetch data
@app.get("/blog",response_model=schema.Show_blog, tags=["Blogs"])
def get_blogs(db:Session = Depends(get_db)):
    blog = db.query(models.Blogs).all()
    return blog

# fetch single data
# response model to fetch specific data
@app.get("/blog/{id}",response_model=schema.Show_blog, tags=["Blogs"])
def get_blogs(id, response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
        # in one liner
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} blog is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data":f"{id} blog is not found"}
    return blog

#remove the data
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete_blog(id, db:Session = Depends(get_db)):
    db.query(models.Blogs).filter(models.Blogs.id == id).delete(synchronize_session=False)
    db.commit()
    return "done"

#update data
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,response_model=schema.Blog, tags=["Blogs"])
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

#create user
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post("/create_user", tags=["Users"])
def create_user(request: schema.User, db:Session = Depends(get_db)):
    user = models.Users(name= request.name, email=request.email, password= pwd_context.hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#fetch user
@app.get("/fetch_user", response_model=List[schema.Show_user], tags=["Users"])
def fetch_user(db:Session = Depends(get_db)):
    user = db.query(models.Users).all()
    return user