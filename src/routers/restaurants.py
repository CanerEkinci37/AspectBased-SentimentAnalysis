import os
from io import BytesIO
import joblib
import pandas as pd
from fastapi import APIRouter, Depends, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .. import dependencies

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

router = APIRouter()

templates = Jinja2Templates(directory=str(BASE_DIR) + "/templates")


with open("./saved_models/restaurant/restaurant_literature1.joblib", "rb") as f:
    RESTAURANT_MODEL = joblib.load(f)


@router.get("/analyze_restaurant/", response_class=HTMLResponse)
def get_restaurant_form(request: Request):
    return templates.TemplateResponse(request=request, name="analyze_restaurant.html")


@router.post("/analyze_restaurant/")
def process_restaurant_form(
    request: Request,
    review_column: str = Form(...),
    csv_file: UploadFile = File(...),
    restaurant_category: dict = Depends(dependencies.get_restaurant_category),
    restaurant_category_count: dict = Depends(
        dependencies.get_restaurant_category_count
    ),
):
    contents = csv_file.file.read()
    data = BytesIO(contents)
    df = pd.read_csv(data)
    data.close()
    csv_file.file.close()
    review_texts = df[review_column].values
    y_preds = RESTAURANT_MODEL.predict(review_texts)
    for pred in y_preds:
        category, sentiment = restaurant_category[pred].split("#")
        restaurant_category_count[category][sentiment] += 1
    context = {"results": restaurant_category_count}
    return templates.TemplateResponse(
        request=request, context=context, name="analyze_restaurant.html"
    )
