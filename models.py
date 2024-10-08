from sqlalchemy import Column, Integer, String
from database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quote = Column(String)
    season = Column(Integer)
    episode = Column(Integer)
    character = Column(String)
