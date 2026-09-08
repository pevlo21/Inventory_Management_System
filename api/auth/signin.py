from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from db.sqlite import session
from models.users import SigninModel, UserBase
from securities.token import bcrypt_context, create_access_token

router_signin = APIRouter()

@router_signin.post("/auth/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: session
):
    user = db.exec(select(UserBase).where(UserBase.username == form_data.username)).first()
    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        username=user.username, user_id=user.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router_signin.post("/signin", response_model=UserBase, status_code=status.HTTP_200_OK)
def signin_user(
    users: SigninModel,
    db: session,
):
    try:
        # Check if the username exists
        user_check = db.exec(select(UserBase).where(UserBase.username == users.username)).first()
        if not user_check:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Username not found",
            )

        if not bcrypt_context.verify(
            users.password,
            user_check.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )
    except Exception:
        db.rollback()
        raise

    return user_check