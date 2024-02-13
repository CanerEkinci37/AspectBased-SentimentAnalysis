from io import BytesIO
import pandas as pd
from fastapi import UploadFile, File
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_restaurant_category():
    category_sentiment_dict = {}

    aspects = ["PRICE", "FOOD", "SERVICE", "AMBIENCE", "MISCELLANEOUS"]
    sentiments = ["NEGATIVE", "NEUTRAL", "POSITIVE"]

    count = 0
    for aspect in aspects:
        for sentiment in sentiments:
            category_sentiment_dict[aspect + "#" + sentiment] = count
            count += 1

    num_to_category_sentiment_restaurant = {}
    for k, v in category_sentiment_dict.items():
        num_to_category_sentiment_restaurant[v] = k
    return num_to_category_sentiment_restaurant


def get_restaurant_category_count():
    restaurant_category_count = {}
    for i in range(15):
        restaurant_category_count[i] = 0
    return restaurant_category_count


async def handle_dataset(dataset: UploadFile = File(...)):
    contents = dataset.file.read()
    data = BytesIO(contents)
    df = pd.read_csv(data)
    data.close()
    dataset.file.close()
    return df
