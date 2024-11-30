from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import SessionLocal, engine, Base
import models

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Pydantic schema for single quote
class QuoteSchema(BaseModel):
    quote: str
    season: int
    episode: int
    character: str

    class Config:
        orm_mode = True  # Enable returning ORM objects as response


# Schema for handling multiple quotes (list of quotes)
class QuotesRequest(BaseModel):
    quotes: List[QuoteSchema]

    class Config:
        orm_mode = True


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET endpoint to fetch quotes with pagination (skip, limit)
@app.get("/getquotes/", response_model=List[QuoteSchema])
def read_quotes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    quotes = db.query(models.Quote).offset(skip).limit(limit).all()
    return quotes


# POST endpoint to create a single quote
@app.post("/createquote/", response_model=QuoteSchema)
def create_quote(quote: QuoteSchema, db: Session = Depends(get_db)):
    db_quote = models.Quote(**quote.dict())  # Convert schema to ORM model
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


# POST endpoint to create multiple quotes at once
@app.post("/createquotes/", response_model=List[QuoteSchema])
def create_multiple_quotes(
    quotes_request: QuotesRequest, db: Session = Depends(get_db)
):
    quotes = []
    for quote in quotes_request.quotes:
        db_quote = models.Quote(**quote.dict())
        db.add(db_quote)
        db.commit()
        db.refresh(db_quote)
        quotes.append(db_quote)
    return quotes
