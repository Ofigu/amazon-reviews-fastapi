import pandas as pd
from sqlalchemy import create_engine

from app.models import Base

DATABASE_URL = "sqlite:///./reviews.db"
CSV_PATH = "data/Amazon_reviews_2023.csv"
CHUNK_SIZE = 500


def seed():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    # Let SQLAlchemy create the table with proper PRIMARY KEY AUTOINCREMENT
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print(f"Reading {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    df["images"] = df["images"].astype(str)
    print(f"Loaded {len(df):,} rows. Writing to database...")

    # index=False: no id column — SQLite assigns it automatically
    df.to_sql("reviews", engine, if_exists="append", index=False, chunksize=CHUNK_SIZE)
    print("Done.")


if __name__ == "__main__":
    seed()
