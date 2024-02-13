from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, dependencies

router = APIRouter()


@router.post(
    "/otel_categories/", tags=["categories"], response_model=schemas.OtelCategory
)
async def create_otel_category(
    category: schemas.OtelCategoryCreate,
    db: Session = Depends(dependencies.get_db),
):
    control = crud.get_otel_category_by_name(
        db=db, category_name=category.category_name
    )
    if control:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_otel_category(db=db, category=category)
