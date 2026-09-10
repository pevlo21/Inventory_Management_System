#from typing import Annotated


from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db.sqlite import session
from models.users import SignupModel, UserBase
from securities.token import bcrypt_context, create_access_token
from services.users import create_user

router_signup = APIRouter()

@router_signup.post("/signup", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def signup_user(
    user: SignupModel,
    db: session
):
    # Check if the username or email already exists
    existing_user = db.exec(
        select(UserBase).where(
            (UserBase.email == user.email) | (UserBase.phone_number == user.phone_number)
        )
    ).first()

    print(f"Existing user: {existing_user}")  # Debugging statement``

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    # Hash the password before storing it
    user.hashed_password = bcrypt_context.hash(user.hashed_password)
    #create access token for the new user
    token = create_access_token(user.username, user.id, timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer", "user": create_user(user, db)}
