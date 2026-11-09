from pydantic import BaseModel


class PermissionModel(BaseModel):
    name: str
    description: str