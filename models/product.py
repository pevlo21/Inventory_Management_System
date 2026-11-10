from enum import Enum

from sqlmodel import Field, SQLModel


class statusE(Enum):
    instock = "instock"
    outofstock = "outofstock"



class ProductBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product: str = Field(index=True)
    category_id: int = Field(foreign_key="categories.id", index=True)
    merchant_id: int = Field(foreign_key="merchants.id", index=True)
    availability: str = Field(index=True)
    instructions: str = Field(index=True)
    price: float = Field(index=True)
    instock: int = Field(index=True)
    status: statusE = Field(index=True)

    __tablename__ = "products"