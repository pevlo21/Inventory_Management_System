from pydantic import BaseModel, EmailStr


class SignupModel(BaseModel):
   first_name: str
   last_name: str
   email: EmailStr
   phone_number: str
   hashed_password: str