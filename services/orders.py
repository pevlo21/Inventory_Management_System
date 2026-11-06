from typing import Annotated

from fastapi import HTTPException, Query, status
from sqlmodel import select

from db.sqlite import session
from models.orders import OrderBase, OrderItem
from models.product import ProductBase
from models.users import UserBase


def place_order(order: OrderBase, db: session):
    #check if the user exists
    existing_user = db.get(UserBase, order.user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    try:
        #check if the product exists
        existing_prod = db.get(ProductBase, order.product_id)
        if not existing_prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="product not found"
            )
        #check if the product is in stock
        if existing_prod.instock < order.Quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='insufficient Stock'
            )       

        #update stock
        existing_prod.instock -= order.Quantity 

    
        #place order
        db.add(order)
        db.commit()
        db.refresh(order)

        return order

    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )


def read_orders(
        db:session,
        offset: int=0,
        limit: Annotated[int,Query(le=100)]=100) -> list[OrderBase]:
    orders = db.exec(select(OrderBase).offset(offset).limit(limit)).all()
    return orders

def read_order(order_id: int, db: session):
    order = db.get(OrderBase, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return order

def cancel_order(order_id: int, db: session):
    order =db.get(OrderBase, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    db.delete(order)
    db.commit()
    return order

