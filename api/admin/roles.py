from typing import Annotated

from fastapi import APIRouter, Depends, status

from db.sqlite import session
from models.roles import Role
from schema.permission import PRModel
from securities.privilage import require_role
from services.roles import create_role, delete_role, read_roles, update_role

router_roles = APIRouter()

@router_roles.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED)
def create_new_role(role: PRModel, db: session, _: Annotated[dict, Depends(require_role("Admin"))]):
    new_role = Role(
        name=role.name,
        description=role.description
    )
    created_role = create_role(new_role, db)
    return created_role

@router_roles.get("/roles", response_model=list[Role])
def list_roles(db: session, _: Annotated[dict, Depends(require_role("Admin"))]):
    roles = read_roles(db)
    return roles

@router_roles.put("/roles/{role_id}", response_model=Role)
def modify_role(role_id: int, role: PRModel, db: session, _: Annotated[dict, Depends(require_role("Admin"))]):
    updated_role = update_role(role_id, role, db)
    return updated_role

@router_roles.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_role(role_id: int, db: session, _: Annotated[dict, Depends(require_role("Admin"))]):
    delete_role(role_id, db)
    return {"detail": "Role deleted successfully"}