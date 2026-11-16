from datetime import datetime

from sqlmodel import Field, SQLModel


class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(index=True, unique=False)
    created_by: datetime= Field(default_factory=datetime.utcnow)
    updated_by: datetime = Field(default_factory=datetime.utcnow)

    __tablename__ = "roles"


class RolePermission(SQLModel, table=True):
    id : int = Field (default=None, primary_key=True)
    role_id :int = Field(default=None, foreign_key="roles.id")
    permission_id:int =Field (default=None, foreign_key="permissions.id")
    created_at : datetime = Field(default_factory=datetime.utcnow)
    upadated_at : datetime =Field(default_factory=datetime.utcnow)


    __tablename__="role_permission"