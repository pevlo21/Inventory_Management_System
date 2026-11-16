from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from datetime import datetime

class MerchantBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    contact_person: str=Field(index=True, unique=False)
    email: EmailStr = Field(index=True, unique=True)
    phone: str = Field(index=True, unique=False)
    address: str = Field(index=True, unique=False)
    status: str = Field(index=True, unique=False)
    region: str = Field(index=True, unique=False)
    created_by: datetime =Field(default_factory=datetime.utcnow)
    updated_by: datetime =Field(default_factory=datetime.utcnow)

    __tablename__ = "merchants"