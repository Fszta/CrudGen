from sqlalchemy import Column, Integer, String


class Test(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False)
    age = Column(Integer, unique=False)
