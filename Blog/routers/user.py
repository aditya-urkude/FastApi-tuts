from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from .. import schema, models
from ..database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

router = APIRouter(tags=["Users"])

#create user
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/create_user")
def create_user(request: schema.User, db:Session = Depends(get_db)):
    user = models.Users(name= request.name, email=request.email, password= pwd_context.hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#fetch user
@router.get("/fetch_user", response_model=List[schema.Show_user])
def fetch_user(db:Session = Depends(get_db)):
    user = db.query(models.Users).all()
    return user