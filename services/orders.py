from typing import Annotated

from fastapi import HTTPException, Query, status
from sqlmodel import select

from db.sqlite import session
from models.orders import OrderBase, OrderItem
from models.product import ProductBase
from models.users import UserBase
from schema.orders import OrderModel


def create_order(order: OrderModel, current_user: UserBase, db: session):

    for item in order.Product_name:

        existing_prod = db.exec(
            select(ProductBase).where(
                ProductBase.product == item.product_name
            )
        ).first()

        if not existing_prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product '{item.product_name}' not found"
            )

        # Check requested quantity
        if existing_prod.instock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {item.product_name}"
            )


def get_order(order_id: int, db: session):
    order = db.get(OrderBase, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return order

def delete_order(order_id: int, db: session):
    order =db.get(OrderBase, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    db.delete(order)
    db.commit()
    return order

