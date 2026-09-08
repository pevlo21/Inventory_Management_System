
from typing import Annotated

from fastapi import Depends, HTTPException, status

from models.users import UserBase
from securities.token import get_current_user


def require_role(required_role: str):
    async def role_checker(
            current_user: Annotated[UserBase, Depends(get_current_user)]):
        if current_user.user_type != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role} privileges required",
            )
        return current_user
    return role_checker