
from sqlmodel import Field, SQLModel
from datetime import datetime

class Warehouse(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    name:str = Field(index=True, unique=True)
    code:str = Field(index=True, unique=True)
    address:str = Field(index=True, unique=False)
    status:str = Field(index=True, unique=False)
    created_by:datetime = Field(default_factory=datetime.utcnow)
    updated_by:datetime = Field(default_factory=datetime.utcnow)


__tablename__ = "warehouses"

class Supply(SQLModel, table=True):
    id: int= Field(default=None, primary_key=True)
    warehouse_id : int =Field(default=None, foreign_key="warehouses.id")
    merchant_id : int = Field(default=None, foreign_key="merchants.id")

    __tablename__="supply"


class WarehouseStock(SQLModel, table=True):
    id : int = Field(default= None, primary_key=True)
    warehouse_id: int =Field(default=None, foreign_key="warehouse.id")
    product_id: int = Field(default= None, foreign_key="products.id")

    __tablename__= "warehouse_stock"