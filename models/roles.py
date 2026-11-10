from sqlmodel import Field, SQLModel


class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(index=True, unique=False)
    created_by: str = Field(index=True, unique=False)
    updated_by: str = Field(index=True, unique=False)

    ___tablename__ = "roles"