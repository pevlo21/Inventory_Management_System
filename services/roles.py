from typing import Annotated

from fastapi import HTTPException, Query, status
from sqlmodel import select

from db.sqlite import session
from models.roles import Role


def create_role(role: Role, db: session):
    try:
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )

def read_roles(
        db:session,
        offset: int=0,
        limit: Annotated[int,Query(le=100)]=100) -> list[Role]:
    roles = db.exec(select(Role).offset(offset).limit(limit)).all()
    return roles

def update_role(role_id: int, role: Role, db: session) -> Role:
    existing_role = db.get(Role, role_id)
    if not existing_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="role not found"
        )
    try:
        for key, value in role.dict(exclude_unset=True).items():
            setattr(existing_role, key, value)
        db.add(existing_role)
        db.commit()
        db.refresh(existing_role)
        return existing_role
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )

def delete_role(role_id: int, db: session):
    existing_role = db.get(Role, role_id)
    if not existing_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="role not found"
        )
    try:
        db.delete(existing_role)
        db.commit()
        return {"message": "role deleted successfully"}
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )