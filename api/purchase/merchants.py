from typing import Annotated

from fastapi import APIRouter, Query, status

from db.sqlite import session
from models.merchant import MerchantBase


router_merchants = APIRouter()

@router_merchants.post("/merchants", response_model=MerchantBase, status_code=status.HTTP_201_CREATED)
def create_merchant(
    merchant: MerchantBase,
    db: session,
):
    db.add(merchant)
    db.commit()
    db.refresh(merchant)
    return merchant

@router_merchants.get("/merchants", response_model=list[MerchantBase], status_code=status.HTTP_200_OK)
def read_all_merchants(
    db: session,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return db.query(MerchantBase).offset(offset).limit(limit).all()