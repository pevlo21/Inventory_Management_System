from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import select

from db.sqlite import session
from models.orders import OrderBase
from models.users import UserBase
from schema.orders import OrderModel
from securities.privilage import require_role
from services.orders import (
    create_order,
    delete_order,
    get_order,
    get_order,
)

role=["user","Admin"]

router_orders = APIRouter()

@router_orders.post("/orders", response_model=OrderBase, status_code=status.HTTP_201_CREATED)
def place_order(
    order: OrderModel,
    db: session,
    current_user: Annotated[UserBase, Depends(require_role(role))]
):

    return create_order(order,current_user, db)

@router_orders.get("/orders", response_model=list[OrderBase])
def read_orders(db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    orders = get_order(db)
    return orders

@router_orders.get("/orders/{order_id}", response_model=OrderBase)
def read_order(order_id: int, db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    order = get_order(order_id, db)
    return order

@router_orders.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(order_id: int, db: session, _:Annotated[dict, Depends(require_role("Admin"))]):
    delete_order(order_id, db)
    return {"detail": "Order cancelled successfully"}