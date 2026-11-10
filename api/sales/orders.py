from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import select

from db.sqlite import session
from models.orders import OrderBase
from schema.orders import OrderModel
from securities.privilage import require_role
from services.orders import (
    create_order,
    delete_order,
    get_order,
    get_orders,
)

router_orders = APIRouter()

@router_orders.post("/orders", response_model=OrderBase, status_code=status.HTTP_201_CREATED)
def place_order(order: OrderModel, db: session, _:Annotated[dict, Depends(require_role("user"))]):

    
    #order placing
    new_order = OrderBase(
        product_name=order.product_name,
        quantity=order.quantity,
        price=order.price,
        customer_id=order.customer_id
    )

    place_order = create_order(new_order, db)
    return place_order

@router_orders.get("/orders", response_model=list[OrderBase])
def read_orders(db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    orders = get_orders(db)
    return orders

@router_orders.get("/orders/{order_id}", response_model=OrderBase)
def read_order(order_id: int, db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    order = get_order(order_id, db)
    return order

@router_orders.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(order_id: int, db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    delete_order(order_id, db)
    return {"detail": "Order cancelled successfully"}