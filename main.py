from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal, engine, Base
import models

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Pydantic schema for validation
class QuoteSchema(BaseModel):
    id: int
    quote: str
    season: int
    episode: int
    character: str

    class Config:
        orm_mode = True


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/quotes/", response_model=list[QuoteSchema])
def read_quotes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    quotes = db.query(models.Quote).offset(skip).limit(limit).all()
    return quotes


@app.post("/quotes/", response_model=QuoteSchema)
def create_quote(quote: QuoteSchema, db: Session = Depends(get_db)):
    db_quote = models.Quote(**quote.dict())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote
