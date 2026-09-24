from enum import Enum

from sqlmodel import Field, SQLModel


class statusE(Enum):
    instock = "instock"
    outofstock = "outofstock"

class ProductBase(SQLModel, table=True):
    product_id: int = Field(default=None, primary_key=True)
    product: str = Field(index=True)
    category: str = Field(index=True)
    availability: str = Field(index=True)
    instock: int = Field(index=True)
    status: statusE = Field(index=True)