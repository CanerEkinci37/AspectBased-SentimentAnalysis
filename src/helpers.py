from io import BytesIO

import joblib
import pandas as pd
from fastapi import UploadFile, File


def handle_dataset(file: UploadFile = File(...)):
    contents = file.file.read()
    data = BytesIO(contents)
    df = pd.read_csv(data)
    data.close()
    file.file.close()
    return df


# Businesses
def get_model(category: str):
    with open(f"./saved_models/{category}/ml_model.joblib", "rb") as f:
        MODEL = joblib.load(f)
    return MODEL


def get_category_sentiments(category: str):
    category_sentiment_dict = {}
    category_count_dict = {}
    sentiments = ["NEGATIVE", "NEUTRAL", "POSITIVE"]

    if category == "restaurant":
        aspects = ["PRICE", "FOOD", "SERVICE", "AMBIENCE", "MISCELLANEOUS"]
    elif category == "otel":
        aspects = ["SERVICE", "MEAL", "LOCATION", "COMFORT", "CLEANLINESS"]
    count = 0
    for aspect in aspects:
        category_count_dict[aspect] = {}
        for sentiment in sentiments:
            category_sentiment_dict[count] = f"{aspect}#{sentiment}"
            category_count_dict[aspect][sentiment] = 0
            count += 1
    return category_sentiment_dict, category_count_dict
