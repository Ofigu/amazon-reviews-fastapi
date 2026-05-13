import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./reviews.db"
CSV_PATH = "data/Amazon_reviews_2023.csv"
CHUNK_SIZE = 500


def seed():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    print(f"Reading {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    df["images"] = df["images"].astype(str)  # store list literal as string
    print(f"Loaded {len(df):,} rows. Writing to database...")

    df.index += 1  # make IDs start at 1
    df.to_sql("reviews", engine, if_exists="replace", index=True, index_label="id", chunksize=CHUNK_SIZE)
    print("Done.")


if __name__ == "__main__":
    seed()
