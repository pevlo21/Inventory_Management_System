from typing import Annotated

from fastapi import HTTPException, Query, status
from sqlmodel import select

from db.sqlite import session
from models.permission import Permission
from models.roles import Role


def create_permission(permission: Permission, db: session):
    try:
        db.add(permission)
        db.commit()
        db.refresh(permission)
        return permission
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )   

def read_permissions(
        db:session,
        offset: int=0,
        limit: Annotated[int,Query(le=100)]=100) -> list[Permission]:
    permissions = db.exec(select(Permission).offset(offset).limit(limit)).all()
    return permissions

def update_permission(permission_id: int, permission: Permission, db: session) -> Permission:
    existing_permission = db.get(Permission, permission_id)
    if not existing_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="permission not found"
        )
    try:
        for key, value in permission.dict(exclude_unset=True).items():
            setattr(existing_permission, key, value)
        db.add(existing_permission)
        db.commit()
        db.refresh(existing_permission)
        return existing_permission
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )

def delete_permission(permission_id: int, db: session):
    existing_permission = db.get(Permission, permission_id)
    if not existing_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="permission not found"
        )
    try:
        db.delete(existing_permission)
        db.commit() 

    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )

