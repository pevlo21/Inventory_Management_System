from pydantic import BaseModel, EmailStr


class SignupModel(BaseModel):
   first_name: str
   last_name: str
   username: str
   email: EmailStr
   phone_number: str
   password: str