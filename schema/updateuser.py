from pydantic import BaseModel, EmailStr


class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    user_type: str | None = None
    phone_number: str | None = None