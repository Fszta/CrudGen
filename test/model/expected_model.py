from sqlalchemy import Column, Integer, String
from database.db_init import Base


class Generated(Base):
    __tablename__ = "generated"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False)
    age = Column(Integer, unique=False)
