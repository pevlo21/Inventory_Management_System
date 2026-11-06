from pydantic import BaseModel


class OrderModel(BaseModel):
    Product_name: str
    Qty : int
    Address: str
    Contact_number: int