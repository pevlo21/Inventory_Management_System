from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from api.auth.token import get_current_user
from db.sqlite import session
from models.users import UserBase
from services.users import create_user, delete_user, read_user, read_users, update_user

router_users = APIRouter()

@router_users.post("/users", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    users: UserBase,
    db: Annotated[session, Depends(session)]
):
    return create_user(users, db)

@router_users.get("/")
def read_all_users(
    db: session,
    _: Annotated[dict, Depends(get_current_user)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return read_users(db, offset, limit)

@router_users.get("/{user_id}")
def read_user_endpoint(
    user_id: int,
    db: session,
    _: Annotated[dict, Depends(get_current_user)],
):
    return read_user(user_id, db)

@router_users.put("/{user_id}", response_model=UserBase)
def update_user_endpoint(
    user_id: int,
    user: UserBase,
    db: session,
    _: Annotated[dict, Depends(get_current_user)],
):
    return update_user(user_id, user, db)

@router_users.delete("/{user_id}")
def delete_user_endpoint(
    user_id: int,
    db: session,
    _: Annotated[dict, Depends(get_current_user)],
):
    return delete_user(user_id, db)