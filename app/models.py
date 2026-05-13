from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=True)
    images = Column(Text, nullable=True)  # JSON string from CSV
    asin = Column(String, index=True)
    parent_asin = Column(String)
    user_id = Column(String)
    timestamp = Column(DateTime)
    helpful_vote = Column(Integer, default=0)
    verified_purchase = Column(Boolean, default=False)
