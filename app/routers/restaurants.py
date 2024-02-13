from enum import Enum
import joblib
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from .. import crud, schemas, dependencies

router = APIRouter()


class RestaurantChoices(str, Enum):
    aspava = "Aspava"
    kofteci_yusuf = "Köfteci Yusuf"


with open("./saved_models/restaurant/restaurant_literature1.joblib", "rb") as f:
    RESTAURANT_MODEL = joblib.load(f)


@router.get(
    "/restaurants/",
    tags=["restaurants"],
)
async def get_restaurant(
    restaurant: RestaurantChoices, db: Session = Depends(dependencies.get_db)
):
    db_restaurant = crud.get_restaurant_by_name(db=db, restaurant_name=restaurant.value)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant does not exist!")
    return {f"details of {restaurant.value}": db_restaurant}


@router.post("/restaurants/", tags=["restaurants"])
async def create_restaurant(
    restaurant_name: str,
    review_column: str,
    df: pd.DataFrame = Depends(dependencies.handle_dataset),
    db: Session = Depends(dependencies.get_db),
    restaurant_category: dict = Depends(dependencies.get_restaurant_category),
    restaurant_category_count: dict = Depends(
        dependencies.get_restaurant_category_count
    ),
) -> dict:
    db_restaurant = crud.get_restaurant_by_name(db=db, restaurant_name=restaurant_name)
    if db_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant already exists")

    results = []

    review_texts = df[review_column].values
    y_preds = RESTAURANT_MODEL.predict(review_texts)
    for pred in y_preds:
        restaurant_category_count[pred] += 1
    for k, v in restaurant_category_count.items():
        results.append(f"{restaurant_category[k]}: {v}")
        crud.create_restaurant(
            db=db,
            restaurant_name=restaurant_name,
            category_id=k + 1,
            category_count=v,
        )
    return {f"results of {restaurant_name}": results}
