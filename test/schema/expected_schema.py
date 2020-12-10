from pydantic import BaseModel


class Test(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True
