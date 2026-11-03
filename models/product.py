from enum import Enum

from sqlmodel import Field, SQLModel


class statusE(Enum):
    instock = "instock"
    outofstock = "outofstock"


class CategoryBase(SQLModel, tabel=True):
    id: int = Field(default=None, primary_key=True)
    category: str = Field(index=True, unique=True)
    description: str = Field(index=True, unique=False)

class ProductBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product: str = Field(index=True)
    category_id: int = Field(foreign_key="CategoryBase.id", index=True)
    merchant_id: int = Field(foreign_key="MerchantBase.id", index=True)
    availability: str = Field(index=True)
    instructions: str = Field(index=True)
    price: float = Field(index=True)
    instock: int = Field(index=True)
    status: statusE = Field(index=True)