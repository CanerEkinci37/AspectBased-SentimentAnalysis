import os

from fastapi import APIRouter, Depends, Form, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import helpers, dependencies, crud

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

router = APIRouter()

templates = Jinja2Templates(directory=str(BASE_DIR) + "/templates")


@router.get("/businesses/", tags=["businesses"], response_class=HTMLResponse)
async def get_business(
    request: Request,
    db: Session = Depends(dependencies.get_db),
):
    db_business = {}
    businesses = crud.get_businesses(db=db)
    for business in businesses:
        business_name = business[0]
        business_category = crud.get_business_category_name(db=db, id=business[1])
        db_business[business_name] = business_category
    context = {"businesses": db_business}
    return templates.TemplateResponse(
        request=request, context=context, name="business.html"
    )


@router.post("/businesses/", tags=["businesses"], response_class=HTMLResponse)
async def post_business(
    request: Request,
    select_businesses: str = Form(...),
    db: Session = Depends(dependencies.get_db),
):
    name = select_businesses.split("-")[0].strip()
    category = select_businesses.split("-")[1].strip()
    category_id = crud.get_business_category_id(db=db, name=category)
    business_id = crud.get_business_id(
        db=db, name=name, business_category_id=category_id
    )

    business_records = crud.get_business_records_by_business(
        db=db, business_id=business_id
    )
    if category == "restaurant":
        _, category_sentiment_count = helpers.get_restaurant_category_sentiments()
    else:
        _, category_sentiment_count = helpers.get_otel_category_sentiments()

    for record in business_records:
        aspect_sentiment_category = crud.get_aspect_sentiment_category_by_id(
            db=db, id=record.aspect_sentiment_category_id
        )
        aspect = crud.get_aspect_category_by_id(
            db=db, id=aspect_sentiment_category.aspect_category_id
        )
        sentiment = crud.get_sentiment_category_by_id(
            db=db, id=aspect_sentiment_category.sentiment_id
        )
        category_sentiment_count[aspect.name.upper()][
            sentiment.name.upper()
        ] = record.count
    context = {"results": category_sentiment_count}
    return templates.TemplateResponse(
        request=request, context=context, name="business.html"
    )


@router.get("/analyze_business/", response_class=HTMLResponse, tags=["businesses"])
def get_analyze_business(request: Request, db: Session = Depends(dependencies.get_db)):
    categories = crud.get_distinct_business_category_names(db=db)
    context = {"business_categories": categories}
    return templates.TemplateResponse(request, "analyze_business.html", context)


@router.post("/analyze_business/", response_class=HTMLResponse, tags=["businesses"])
def post_analyze_business(
    request: Request,
    selected_category: str = Form(...),
    column: str = Form(...),
    file: UploadFile = File(...),
):
    df = helpers.handle_dataset(file)
    reviews = df[column].values
    preds = helpers.get_model(selected_category).predict(reviews)
    categories, category_counts = helpers.get_category_sentiments(selected_category)

    for pred in preds:
        category, sentiment = categories[pred].split("#")
        category_counts[category][sentiment] += 1
    context = {"results": category_counts}
    return templates.TemplateResponse(request, "analyze_business.html", context)


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
