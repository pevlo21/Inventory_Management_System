from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_name: str
    quantity: int


class OrderModel(BaseModel):
    Product_name: list[OrderItemCreate]
    Address: str
    Contact_number: int