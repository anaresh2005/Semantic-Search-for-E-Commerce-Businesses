import pandas as pd


def parse_ratings_count(ratings: str) -> int | None:
    if pd.isna(ratings):
        return 0
    try:
        ratings_parsed = ratings.split()[0].replace(",", "").replace(".", "")
        return int(ratings_parsed)
    except (ValueError, IndexError):
        return 0


def parse_stars_count(stars: str) -> float | None:
    if pd.isna(stars):
        return -1.0
    try:
        stars_parsed = stars.split()[0].replace(",", ".")
        return float(stars_parsed)
    except (ValueError, IndexError):
        return -1.0


def parse_price(price: str) -> float | None:
    if pd.isna(price):
        return None
    try:
        price_parsed = price.replace("€", "").replace("$", "").replace(",", ".")
        return float(price_parsed)
    except (ValueError, IndexError):
        return None


def process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df_processed = df.copy()
    df_processed = df_processed[df_processed["locale"] == "us"]

    columns = [
        "asin",
        "type",
        "category",
        "title",
        "description",
        "stars",
        "ratings",
        "price",
    ]

    df_processed = df_processed[columns]

    df_processed["review_count"] = df_processed["ratings"].apply(parse_ratings_count)
    df_processed["review_ratings"] = df_processed["stars"].apply(parse_stars_count)
    df_processed["price"] = df_processed["price"].apply(parse_price)

    df_processed = df_processed.dropna(subset=["price"]).astype(
        {
            "asin": str,
            "type": str,
            "category": str,
            "title": str,
            "description": str,
            "review_ratings": float,
            "review_count": int,
            "price": float,
        }
    )

    return df_processed.reset_index(drop=True)
