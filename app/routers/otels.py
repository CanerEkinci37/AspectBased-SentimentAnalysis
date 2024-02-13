from enum import Enum
import joblib
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from .. import crud, schemas, dependencies

router = APIRouter()


class OtelChoices(str, Enum):
    pass


with open("./saved_models/otel/otel_literature1.joblib", "rb") as f:
    OTEL_MODEL = joblib.load(f)


@router.get(
    "/otels/",
    tags=["otels"],
)
async def get_otel(otel: OtelChoices, db: Session = Depends(dependencies.get_db)):
    db_otel = crud.get_otel_by_name(db=db, otel_name=otel.value)
    if not db_otel:
        raise HTTPException(status_code=404, detail="Otel does not exist!")
    return {f"details of {otel.value}": db_otel}


@router.post("/otels/", tags=["otels"])
async def create_otel(
    otel_name: str,
    review_column: str,
    df: pd.DataFrame = Depends(dependencies.handle_dataset),
    db: Session = Depends(dependencies.get_db),
    otel_category: dict = Depends(dependencies.get_otel_category),
    otel_category_count: dict = Depends(dependencies.get_restaurant_category_count),
) -> dict:
    db_otel = crud.get_otel_by_name(db=db, otel_name=otel_name)
    if db_otel:
        raise HTTPException(status_code=400, detail="Otel already exists")

    results = []

    review_texts = df[review_column].values
    y_preds = OTEL_MODEL.predict(review_texts)
    for pred in y_preds:
        otel_category_count[pred] += 1
    for k, v in otel_category_count.items():
        results.append(f"{otel_category[k]}: {v}")
        crud.create_otel(
            db=db, otel_name=otel_name, otel_category_id=k + 1, category_count=v
        )
    return {f"results of {otel_name}": results}
