from typing import Annotated

from fastapi import APIRouter, Query, status

from db.sqlite import session
from models.category import Category as CategoryBase

router_category = APIRouter()

@router_category.post("/category", response_model=CategoryBase, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryBase,
    db: session,
):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router_category.get("/category", response_model=list[CategoryBase], status_code=status.HTTP_200_OK)
def read_all_categories(
    db: session,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return db.query(CategoryBase).offset(offset).limit(limit).all()

