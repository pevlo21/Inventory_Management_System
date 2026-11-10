from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from db.sqlite import session
from securities.privilage import require_role
from models.product import ProductBase
from schema.updateuser import UpdateProduct
from services.products import create_product, read_product, read_products, update_product, delete_product

router_product = APIRouter()

@router_product.post("/products", response_model=ProductBase, status_code=status.HTTP_201_CREATED)
def add_products(
    prod:ProductBase,
    db:session,
    _: Annotated[dict, Depends(require_role("Admin"))]
    ):
    return create_product(prod,db)
    

@router_product.get("/")
def read_all_products(
    db: session,
    offset: int =0,
    limit: Annotated[int, Query(le=100)] =100
):
    return read_product(db, offset, limit)


@router_product.get("/{product_id}")
def read_one_product(
    product_id: int,
    db:session,
):
    return read_product(product_id,db)

@router_product.put("/{product_id}", response_model=ProductBase)
def modify_product(
    product_id: int,
    prod: UpdateProduct,
    db: session,
    _: Annotated[dict, Depends(require_role("Admin"))],
):
    return update_product(product_id,prod,db)

