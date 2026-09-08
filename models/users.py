from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    user_type: str = Field(default="user")  # Default user type is "user"
    email: EmailStr = Field(index=True, unique=False)
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})  # Store hashed password

class SigninModel(SQLModel):
    email: EmailStr
    password: str
    remember_me: bool  # Optional field for "remember me" functionality

class SignupModel(SQLModel):
    username: str
    email: EmailStr
    password: str