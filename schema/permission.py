from pydantic import BaseModel


class PRModel(BaseModel):
    name: str
    description: str