from pydantic import BaseModel


class Test(BaseModel):
    name: str
    age: int
    img_url: str
    description: str
