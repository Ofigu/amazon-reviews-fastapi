# Amazon Reviews FastAPI

A REST API for querying and managing Amazon product reviews, built with FastAPI and SQLite.

## Dataset

Download `Amazon_reviews_2023.csv` from [Kaggle](https://www.kaggle.com/datasets/ravirajbabasomane/amazon-reviews-2023) and place it in the `data/` folder.

## Setup

```bash
pip install -r requirements.txt
```

Seed the database (only needed once):

```bash
python seed.py
```

This loads `data/Amazon_reviews_2023.csv` (~700k rows) into `reviews.db`.

## Running

```bash
fastapi dev app/main.py
```

Interactive docs available at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/reviews` | List reviews with optional filters |
| GET | `/reviews/{id}` | Get a single review by ID |
| POST | `/reviews` | Create a new review |
| PUT | `/reviews/{id}` | Update fields on an existing review |
| DELETE | `/reviews/{id}` | Delete a review |

### GET /reviews — query params

| Param | Type | Description |
|-------|------|-------------|
| `limit` | int | Max results (default 20, max 100) |
| `offset` | int | Skip N rows for pagination |
| `asin` | string | Filter by product ASIN |
| `rating` | int | Filter by rating (1-5) |
| `verified_purchase` | bool | Filter by verified purchase status |

## Data model

| Field | Type |
|-------|------|
| `id` | int (auto) |
| `rating` | int |
| `title` | string |
| `text` | string |
| `images` | string |
| `asin` | string |
| `parent_asin` | string |
| `user_id` | string |
| `timestamp` | datetime |
| `helpful_vote` | int |
| `verified_purchase` | bool |
