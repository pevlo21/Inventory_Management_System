from pydantic import BaseModel, EmailStr


class SigninModel(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False  # Optional field for "remember me" functionality
