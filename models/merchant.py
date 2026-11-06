from sqlmodel import Field, SQLModel


class MerchantBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    contact_person: str=Field(index=True, unique=False)
    email: str = Field(index=True, unique=True)
    phone: str = Field(index=True, unique=False)
    address: str = Field(index=True, unique=False)
    status: str = Field(index=True, unique=False)
    region: str = Field(index=True, unique=False)
    created_by: str = Field(index=True, unique=False)
    updated_by: str = Field(index=True, unique=False)