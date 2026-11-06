from sqlmodel import Field, SQLModel


class category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    category: str = Field(index=True, unique=True)
    description: str = Field(index=True, unique=False)