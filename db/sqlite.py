from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

db_name="inventory.db"
url=f"sqlite:///{db_name}"

engine=create_engine(url)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

session=Annotated[Session,Depends(get_session)]