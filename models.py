from pydantic import BaseModel


class Trinket(BaseModel):
    title: str
    code: str
