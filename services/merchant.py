from typing import Annotated

from fastapi import HTTPException, Query, status
from sqlmodel import select

from db.sqlite import session
from models.merchant import MerchantBase
from models.users import UserBase


def add_merchant(merchant: MerchantBase, db: session):
    #check if the user exists
    existing_user = db.get(UserBase, merchant.created_by)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    try:
        #check if the merchant already exists
        existing_merchant = db.exec(select(MerchantBase).where(MerchantBase.name == merchant.name)).first()
        if existing_merchant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="merchant already exists"
            )
        #add merchant
        db.add(merchant)
        db.commit()
        db.refresh(merchant)

        return merchant

    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )


def read_merchants(
        db:session,
        offset: int=0,
        limit: Annotated[int,Query(le=100)]=100) -> list[MerchantBase]:
    merchants = db.exec(select(MerchantBase).offset(offset).limit(limit)).all()
    return merchants

def read_merchant(merchant_id: int, db: session) -> MerchantBase:
    merchant = db.get(MerchantBase, merchant_id)
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="merchant not found"
        )
    return merchant

def update_merchant(merchant_id: int, merchant: MerchantBase, db: session) -> MerchantBase:
    existing_merchant = db.get(MerchantBase, merchant_id)
    if not existing_merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="merchant not found"
        )
    try:
        #update merchant
        existing_merchant.name = merchant.name
        existing_merchant.contact_person = merchant.contact_person
        existing_merchant.email = merchant.email
        existing_merchant.phone = merchant.phone
        existing_merchant.address = merchant.address
        existing_merchant.status = merchant.status
        existing_merchant.region = merchant.region
        existing_merchant.updated_by = merchant.updated_by

        db.add(existing_merchant)
        db.commit()
        db.refresh(existing_merchant)

        return existing_merchant

    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )

def delete_merchant(merchant_id: int, db: session):
    existing_merchant = db.get(MerchantBase, merchant_id)
    if not existing_merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="merchant not found"
        )
    try:
        #delete merchant
        db.delete(existing_merchant)
        db.commit()

        return {"detail": "merchant deleted successfully"}

    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )
    