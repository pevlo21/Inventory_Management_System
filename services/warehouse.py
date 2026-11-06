from typing import Annotated

from fastapi import HTTPException, Query, status
from models.warehouse import Warehouse
from sqlmodel import select

from db.sqlite import session


def create_warehouse(warehouse: Warehouse, db: session):
    try:
        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)
        return warehouse
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )


def read_warehouses(
        db: session,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
) -> list[Warehouse]:
    warehouses = db.exec(select(Warehouse).offset(offset).limit(limit)).all()
    return warehouses


def update_warehouse(warehouse_id: int, warehouse: Warehouse, db: session) -> Warehouse:
    existing_warehouse = db.get(Warehouse, warehouse_id)
    if not existing_warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    try:
        for key, value in warehouse.dict(exclude_unset=True).items():
            setattr(existing_warehouse, key, value)
        db.add(existing_warehouse)
        db.commit()
        db.refresh(existing_warehouse)
        return existing_warehouse
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )


def delete_warehouse(warehouse_id: int, db: session):
    existing_warehouse = db.get(Warehouse, warehouse_id)
    if not existing_warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    try:
        db.delete(existing_warehouse)
        db.commit()

    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )
