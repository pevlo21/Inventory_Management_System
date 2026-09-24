from typing import Annotated

from fastapi import HTTPException, Query, status
from sqlmodel import select

from db.sqlite import session
from models.product import ProductBase


def create_user(product: ProductBase, db: session):
    try:
        #check if the product already exists
        existing_prod = db.exec(select(ProductBase).where(ProductBase.product_id == product.product_id)).first()
        if existing_prod:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already exists"
            )
        #create new product
        db.add(product)
        db.commit(product)
        db.refresh(product)
        return product

    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )
    return product

def read_products(
        db: session,
        offset: int=0,
        limit: Annotated[int,Query(le=100)] = 100
    ) -> list[ProductBase]:
    products= db.exec(select(ProductBase).offset(offset).limit(limit)).all()
    return products

def read_product(product_id: int, db: session):
    prod = db.get(ProductBase,product_id)
    if not prod:
        raise HTTPException(status_code=404,detail="product not found")
    return prod

def update_product(
        prod_id: int,
        prod: ProductBase,
        db: session
) -> ProductBase:
    existing_prod = db.get(ProductBase,prod_id)
    if not existing_prod:
        raise  HTTPException(status_code=404,detail="product not found")

    for field, value in prod.dict(exclude_unset=True).items():
        setattr(existing_prod,field,value)

    db.add(existing_prod)
    db.commit()
    db.refresh(existing_prod)
    return existing_prod

def delete_product(prod_id: int, db: session):
    prod = db.get(ProductBase,prod_id)
    if not prod:
        raise HTTPException(status_code=404,detail="product not found")
    db.delete(prod)
    db.commit()
    return {"ok":True}

