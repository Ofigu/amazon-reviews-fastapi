from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class ReviewSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    rating: int
    title: str
    text: str = None
    images: str = None
    asin: str
    parent_asin: str
    user_id: str
    timestamp: datetime
    helpful_vote: int
    verified_purchase: bool


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/reviews", response_model=list[ReviewSchema])
def get_reviews(
    limit: int = Query(20, le=100),
    offset: int = Query(0),
    db: Session = Depends(get_db),
):
    return db.query(models.Review).offset(offset).limit(limit).all()


@app.get("/reviews/{review_id}", response_model=ReviewSchema)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


