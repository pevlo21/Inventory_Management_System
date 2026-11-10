from datetime import date as Date
from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class statusE(Enum):
    pending = "pending"
    shipped = "shipped"
    delayed = "delayed"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(index=True)

    __tablename__ = "order_items"

class OrderBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: Date = Field(default_factory=lambda: datetime.now(tz=timezone.utc).date())
    user_id: int = Field(foreign_key="users.id")
    sales_channel: str = Field(index=True)
    destination: str = Field(index=True)
    item: str = Field(index=True)
    status: statusE = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    __tablename__ = "orders"