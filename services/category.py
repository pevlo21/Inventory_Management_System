from typing import Annotated

from fastapi import HTTPException, Query, status
from sqlmodel import select

from db.sqlite import session
from models.category import Category


def create_category(category: Category, db: session):
    try:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )   

def read_categories(
        db:session,
        offset: int=0,
        limit: Annotated[int,Query(le=100)]=100) -> list[Category]:
    categories = db.exec(select(Category).offset(offset).limit(limit)).all()
    return categories

def update_category(category_id: int, category: Category, db: session) -> Category:
    existing_category = db.get(Category, category_id)
    if not existing_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category not found"
        )
    try:
        for key, value in category.dict(exclude_unset=True).items():
            setattr(existing_category, key, value)
        db.add(existing_category)
        db.commit()
        db.refresh(existing_category)
        return existing_category
    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )

def delete_category(category_id: int, db: session):
    existing_category = db.get(Category, category_id)
    if not existing_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category not found"
        )
    try:
        db.delete(existing_category)
        db.commit()

    except Exception as e:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(e)
        )

    