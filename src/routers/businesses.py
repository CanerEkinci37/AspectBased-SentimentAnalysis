import os

from fastapi import APIRouter, Depends, Form, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import helpers, dependencies, crud

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

router = APIRouter()

templates = Jinja2Templates(directory=str(BASE_DIR) + "/templates")


# Analyzes


@router.get("/analyze_restaurant/", response_class=HTMLResponse, tags=["businesses"])
def get_restaurant_form(request: Request):
    return templates.TemplateResponse(request=request, name="analyze_restaurant.html")


@router.post("/analyze_restaurant/", response_class=HTMLResponse, tags=["businesses"])
def process_restaurant_form(
    request: Request,
    review_column: str = Form(...),
    csv_file: UploadFile = File(...),
):
    df = helpers.handle_dataset(csv_file)
    review_texts = df[review_column].values
    y_preds = helpers.get_restaurant_model().predict(review_texts)
    restaurant_category, restaurant_category_count = (
        helpers.get_restaurant_category_sentiments()
    )
    for pred in y_preds:
        category, sentiment = restaurant_category[pred].split("#")
        restaurant_category_count[category][sentiment] += 1
    context = {"results": restaurant_category_count}
    return templates.TemplateResponse(
        request=request, context=context, name="analyze_restaurant.html"
    )


@router.get("/analyze_otel/", response_class=HTMLResponse, tags=["businesses"])
def get_otel_form(request: Request):
    return templates.TemplateResponse(request=request, name="analyze_otel.html")


@router.post("/analyze_otel/", tags=["businesses"])
def process_otel_form(
    request: Request,
    review_column: str = Form(...),
    csv_file: UploadFile = File(...),
):
    df = helpers.handle_dataset(csv_file)
    review_texts = df[review_column].values
    y_preds = helpers.get_otel_model().predict(review_texts)
    otel_category, otel_category_count = helpers.get_otel_category_sentiments()
    for pred in y_preds:
        category, sentiment = otel_category[pred].split("#")
        otel_category_count[category][sentiment] += 1
    context = {"results": otel_category_count}
    return templates.TemplateResponse(
        request=request, context=context, name="analyze_restaurant.html"
    )


# Businesses


@router.get("/businesses/", tags=["businesses"])
async def get_business(
    business_category: str,
    business_name: str,
    db: Session = Depends(dependencies.get_db),
):
    business_category_id = crud.get_business_category_id(db=db, name=business_category)
    if business_category_id:
        business_id = crud.get_business_id(
            db=db, name=business_name, business_category_id=business_category_id
        )
        if business_id:
            if business_category == "restaurant":
                _, category_sentiment_count = (
                    helpers.get_restaurant_category_sentiments()
                )
            else:
                _, category_sentiment_count = helpers.get_otel_category_sentiments()
            for aspect, sentiments in category_sentiment_count.items():
                aspect_category_id = crud.get_aspect_category_id(
                    db=db, name=aspect, business_category_id=business_category_id
                )
                for sentiment in sentiments:
                    sentiment_id = crud.get_sentiment_category_id(db=db, name=sentiment)
                    aspect_sentiment_category_id = (
                        crud.get_aspect_sentiment_category_id(
                            db=db,
                            sentiment_id=sentiment_id,
                            aspect_category_id=aspect_category_id,
                        )
                    )
                    business_record = crud.get_business_record(
                        db=db,
                        business_id=business_id,
                        aspect_sentiment_category_id=aspect_sentiment_category_id,
                    )
                    category_sentiment_count[aspect][sentiment] = business_record.count
            return {f"{business_name.title()}": category_sentiment_count}
        raise HTTPException(
            status_code=404,
            detail=f"There is not such a {business_name.title()} business name",
        )
    raise HTTPException(
        status_code=404,
        detail=f"There is not like {business_category.title()} business category",
    )


@router.get("/compare_businesses/", tags=["businesses"])
async def compare_businesses(
    business_category: str,
    business_name_first: str,
    business_name_second: str,
    db: Session = Depends(dependencies.get_db),
):
    business_category_id = crud.get_business_category_id(db=db, name=business_category)
    if business_category_id:
        business_first_id = crud.get_business_id(
            db=db, name=business_name_first, business_category_id=business_category_id
        )
        business_second_id = crud.get_business_id(
            db=db, name=business_name_second, business_category_id=business_category_id
        )
        if business_first_id is not None and business_second_id is not None:
            if business_category == "restaurant":
                _, category_sentiment_count_first = (
                    helpers.get_restaurant_category_sentiments()
                )
                _, category_sentiment_count_second = (
                    helpers.get_restaurant_category_sentiments()
                )
            else:
                _, category_sentiment_count_first = (
                    helpers.get_otel_category_sentiments()
                )
                _, category_sentiment_count_second = (
                    helpers.get_otel_category_sentiments()
                )
            for aspect, sentiments in category_sentiment_count_first.items():
                aspect_category_id = crud.get_aspect_category_id(
                    db=db, name=aspect, business_category_id=business_category_id
                )
                for sentiment in sentiments:
                    sentiment_id = crud.get_sentiment_category_id(db=db, name=sentiment)
                    aspect_sentiment_category_id = (
                        crud.get_aspect_sentiment_category_id(
                            db=db,
                            sentiment_id=sentiment_id,
                            aspect_category_id=aspect_category_id,
                        )
                    )
                    business_record_first = crud.get_business_record(
                        db=db,
                        business_id=business_first_id,
                        aspect_sentiment_category_id=aspect_sentiment_category_id,
                    )
                    business_record_second = crud.get_business_record(
                        db=db,
                        business_id=business_second_id,
                        aspect_sentiment_category_id=aspect_sentiment_category_id,
                    )
                    category_sentiment_count_first[aspect][
                        sentiment
                    ] = business_record_first.count
                    category_sentiment_count_second[aspect][
                        sentiment
                    ] = business_record_second.count
            return {
                f"{business_name_first.title()}": category_sentiment_count_first,
                f"{business_name_second.title()}": category_sentiment_count_second,
            }
        raise HTTPException(
            status_code=404,
            detail="One of the business names are wrong or in wrong business category",
        )
    raise HTTPException(
        status_code=404,
        detail=f"There is not like {business_category.title()} business category",
    )


@router.post("/create_business/", tags=["businesses"])
async def create_business(
    business_category: str,
    business_name: str,
    review_column: str = Form(...),
    csv_file: UploadFile = File(...),
    db: Session = Depends(dependencies.get_db),
):
    business_category_id = crud.get_business_category_id(db=db, name=business_category)
    if business_category_id:
        business_id = crud.get_business_id(
            db=db, name=business_name, business_category_id=business_category_id
        )
        if business_id:
            raise HTTPException(
                status_code=400,
                detail=f"{business_name.title()} already exists for {business_category.title()}",
            )
        crud.create_business(
            db=db,
            business_name=business_name,
            business_category_id=business_category_id,
        )
        df = helpers.handle_dataset(csv_file)
        review_texts = df[review_column].values
        if business_category.lower() == "restaurant":
            y_preds = helpers.get_restaurant_model().predict(review_texts)
            business_category, business_category_count = (
                helpers.get_restaurant_category_sentiments()
            )
        else:
            y_preds = helpers.get_otel_model().predict(review_texts)
            business_category, business_category_count = (
                helpers.get_otel_category_sentiments()
            )
        business_id_new = crud.get_business_id(
            db=db, name=business_name, business_category_id=business_category_id
        )
        for pred in y_preds:
            category, sentiment = business_category[pred].split("#")
            business_category_count[category][sentiment] += 1
        for aspect, sentiments in business_category_count.items():
            aspect_id = crud.get_aspect_category_id(
                db=db, name=aspect, business_category_id=business_category_id
            )
            for sentiment_str in sentiments.keys():
                sentiment_id = crud.get_sentiment_category_id(db=db, name=sentiment_str)
                aspect_sentiment_category_id = crud.get_aspect_sentiment_category_id(
                    db=db,
                    sentiment_id=sentiment_id,
                    aspect_category_id=aspect_id,
                )
                crud.create_business_record(
                    db=db,
                    business_id=business_id_new,
                    aspect_sentiment_category_id=aspect_sentiment_category_id,
                    count=sentiments[sentiment_str],
                )
        return {"message": f"{business_name} records successfully created"}
    raise HTTPException(status_code=404, detail="Business category does not found")
