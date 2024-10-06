from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


class QuoteSchema(BaseModel):
    quote: str
    season: int
    episode: int
    character: str

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/getquotes/", response_model=list[QuoteSchema])
def read_quotes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    quotes = db.query(models.Quote).offset(skip).limit(limit).all()
    return quotes


@app.post("/createquotes/", response_model=QuoteSchema)
def create_quote(quote: QuoteSchema, db: Session = Depends(get_db)):
    db_quote = models.Quote(**quote.dict())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote
