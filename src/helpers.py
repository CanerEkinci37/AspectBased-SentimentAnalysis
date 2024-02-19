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


# Restaurants


def get_restaurant_model():
    with open("./saved_models/restaurant/restaurant_literature1.joblib", "rb") as f:
        RESTAURANT_MODEL = joblib.load(f)
    return RESTAURANT_MODEL


def get_restaurant_category_sentiments():
    category_sentiment_dict = {}
    category_count_dict = {}

    aspects = ["PRICE", "FOOD", "SERVICE", "AMBIENCE", "MISCELLANEOUS"]
    sentiments = ["NEGATIVE", "NEUTRAL", "POSITIVE"]

    count = 0
    for aspect in aspects:
        category_count_dict[aspect] = {}
        for sentiment in sentiments:
            category_sentiment_dict[count] = f"{aspect}#{sentiment}"
            category_count_dict[aspect][sentiment] = 0
            count += 1
    return category_sentiment_dict, category_count_dict


# Otels


def get_otel_model():
    with open("./saved_models/otel/otel_literature1.joblib", "rb") as f:
        OTEL_MODEL = joblib.load(f)
    return OTEL_MODEL


def get_otel_category_sentiments():
    category_sentiment_dict = {}
    category_count_dict = {}

    aspects = ["SERVICE", "MEAL", "LOCATION", "COMFORT", "CLEANLINESS"]
    sentiments = ["NEGATIVE", "NEUTRAL", "POSITIVE"]

    count = 0
    for aspect in aspects:
        category_count_dict[aspect] = {}
        for sentiment in sentiments:
            category_sentiment_dict[count] = f"{aspect}#{sentiment}"
            category_count_dict[aspect][sentiment] = 0
            count += 1
    return category_sentiment_dict, category_count_dict
