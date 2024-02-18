import os
from io import BytesIO
import joblib
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .. import dependencies

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

router = APIRouter()

templates = Jinja2Templates(directory=str(BASE_DIR) + "/templates")

with open("./saved_models/otel/otel_literature1.joblib", "rb") as f:
    OTEL_MODEL = joblib.load(f)


@router.get("/analyze_otel/", response_class=HTMLResponse)
def get_otel_form(request: Request):
    return templates.TemplateResponse(request=request, name="analyze_otel.html")


@router.post("/analyze_otel/")
def process_otel_form(
    request: Request,
    review_column: str = Form(...),
    csv_file: UploadFile = File(...),
    otel_category: dict = Depends(dependencies.get_otel_category),
    otel_category_count: dict = Depends(dependencies.get_otel_category_count),
):
    contents = csv_file.file.read()
    data = BytesIO(contents)
    df = pd.read_csv(data)
    data.close()
    csv_file.file.close()
    review_texts = df[review_column].values
    y_preds = OTEL_MODEL.predict(review_texts)
    for pred in y_preds:
        category, sentiment = otel_category[pred].split("#")
        otel_category_count[category][sentiment] += 1
    context = {"results": otel_category_count}
    return templates.TemplateResponse(
        request=request, context=context, name="analyze_restaurant.html"
    )
