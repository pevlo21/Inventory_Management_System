
from sqlmodel import Field, SQLModel

class WarehouseBase(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    name:str = Field(index=True, unique=True)
    code:str = Field(index=True, unique=True)
    address:str = Field(index=True, unique=False)
    status:str = Field(index=True, unique=False)
    created_by:str = Field(index=True, unique=False)
    updated_by:str = Field(index=True, unique=False)