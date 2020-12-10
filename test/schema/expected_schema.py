from pydantic import BaseModel


class Test(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True
