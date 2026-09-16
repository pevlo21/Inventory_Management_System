#from typing import Annotated


from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db.sqlite import session
from models.users import UserBase
from schema.signup import SignupModel
from securities.token import bcrypt_context, create_access_token
from services.users import create_user

router_signup = APIRouter()

@router_signup.post("/signup", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def signup_user(
    user: SignupModel,
    db: session
):
    # Check if email or phone number already exists
    existing_user = db.exec(
        select(UserBase).where(
            (UserBase.email == user.email) |
            (UserBase.phone_number == user.phone_number)
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or phone number already exists"
        )

    # Create UserBase object
    new_user = UserBase(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=bcrypt_context.hash(user.password)
    )

    # Save user to database
    save_user = create_user(new_user, db)

    # Create access token after database generates the ID
    _ = create_access_token(
        save_user.username,
        save_user.id,
        timedelta(minutes=30)
    )

    return save_user