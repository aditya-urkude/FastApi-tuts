from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema, models
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from . import token

router = APIRouter(tags=["Autentication"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login_user(request :schema.Authenticaton ,db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.email).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=" Invalid Credentails user not found!")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invalid password Try Again!!!")
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return schema.Token(access_token=access_token, token_type="bearer")

