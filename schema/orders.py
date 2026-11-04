from pydantic import BaseModel


class OrderModel(BaseModel):
    product_name: str
    qty : int
    