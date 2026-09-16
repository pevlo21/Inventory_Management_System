from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    username: str = Field(index=True, unique=True)
    user_type: str = Field(default="user")  # Default user type is "user"
    phone_number: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=False)
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})  # Store hashed password