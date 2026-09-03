from typing import Annotated

from fastapi import HTTPException, Query, status
from sqlmodel import select

from db.sqlite import session
from models.users import UserBase


def create_user(users: UserBase, db: session):
    try:
        # Check if the username already exists
        existing_user = db.exec(select(UserBase).where(UserBase.username == users.username)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        # Create a new user
        db.add(users)
        db.commit()
        db.refresh(users)
        return users
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
            )
    return users

def read_users(
    db: session,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[UserBase]:
    users = db.exec(select(UserBase).offset(offset).limit(limit)).all()
    return users

def read_user(user_id: int, db: session) -> UserBase:
    user = db.get(UserBase, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user(user_id: int, db: session):
    user = db.get(UserBase, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}

def update_user(
    user_id: int,
    user: UserBase,
    db: session
) -> UserBase:
    existing_user = db.get(UserBase, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the fields of the existing user with the new values
    for field, value in user.dict(exclude_unset=True).items():
        setattr(existing_user, field, value)

    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    return existing_user