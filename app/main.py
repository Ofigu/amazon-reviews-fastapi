from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class ReviewSchemaOut(BaseModel):
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

class ReviewSchemaUpdate(BaseModel):
    model_config = {"from_attributes": True}

    rating: int | None = None
    title: str = None
    text: str = None
    images: str = None
    asin: str = None
    parent_asin: str = None
    user_id: str = None
    timestamp: datetime = None
    helpful_vote: int = None
    verified_purchase: bool = None

class ReviewSchemaIn(BaseModel):
    model_config = {"from_attributes": True}

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


#get specific review/s by filter
@app.get("/reviews", response_model=list[ReviewSchemaOut])
def get_reviews_filtered_test(
    limit: int = Query(20, le = 100),
    offset: int = Query(0),
    asin: str | None = Query(None),
    rating: int | None = Query(None),
    verified_purchase: bool | None = Query(None),
    db: Session = Depends(get_db)
):
    
    q = db.query(models.Review)
    if asin:
        q = q.filter(models.Review.asin == asin)
    if rating:
        q = q.filter(models.Review.rating == rating)
    if verified_purchase is not None:
        q = q.filter(models.Review.verified_purchase == verified_purchase)
    return q.offset(offset).limit(limit).all()

#post new review
@app.post("/reviews", response_model=ReviewSchemaOut, status_code=201)
def add_review(review: ReviewSchemaIn, db: Session = Depends(get_db)):
    db_review = models.Review(**review.model_dump())
    db.add(db_review) #creating db object - staging
    db.commit() #writing to db
    db.refresh(db_review) #rereads the row from db back into db_review - now with an id assign to
    return db_review

#get specific review
@app.get("/reviews/{review_id}", response_model=ReviewSchemaOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

#modify exsiting review
@app.put("/reviews/{review_id}", response_model=ReviewSchemaOut)
def update_review(
    review_id: int,
    updates: ReviewSchemaUpdate,
    db: Session = Depends(get_db)):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review

@app.delete("/reviews/{review_id}", status_code=200)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"detail": f"review {review_id} deleted"}
 
