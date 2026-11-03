from sqlmodel import Field, SQLModel


class MerchantBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    merchant: str = Field(index=True, unique=True)
    region: str = Field(index=True, unique=False)
