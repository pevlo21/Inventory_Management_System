from typing import Annotated

from fastapi import APIRouter, Depends, status

from db.sqlite import session
from models.permission import Permission
from schema.permission import PermissionModel
from securities.privilage import require_role
from services.permission import (
    create_permission,
    delete_permission,
    read_permissions,
    update_permission,
)

router_permission = APIRouter()

@router_permission.post("/permissions", response_model=Permission, status_code=status.HTTP_201_CREATED)
def add_permission(permission: PermissionModel, db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    new_permission = Permission(
        name=permission.name,
        description=permission.description
    )
    created_permission = create_permission(new_permission, db)
    return created_permission

@router_permission.get("/permissions", response_model=list[Permission])
def get_permissions(db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    permissions = read_permissions(db)
    return permissions

@router_permission.put("/permissions/{permission_id}", response_model=Permission)
def modify_permission(permission_id: int, permission: PermissionModel, db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    updated_permission = update_permission(permission_id, permission, db)
    return updated_permission   

@router_permission.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_permission(permission_id: int, db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    delete_permission(permission_id, db)
    return {"detail": "Permission deleted successfully"}