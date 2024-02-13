from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, dependencies

router = APIRouter()


@router.post(
    "/restaurant_categories/",
    tags=["categories"],
)
async def create_restaurant_category(
    category: schemas.RestaurantCategoryCreate,
    db: Session = Depends(dependencies.get_db),
):
    control = crud.get_restaurant_category_by_name(
        db=db, category_name=category.category_name
    )
    if control:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_restaurant_category(db=db, category=category)
