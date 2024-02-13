from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, dependencies

router = APIRouter()


@router.post("/categories/", tags=["categories"], response_model=schemas.Category)
async def create_category(
    category: schemas.CategoryCreate, db: Session = Depends(dependencies.get_db)
):
    db_category = crud.get_category_id_by_name(db, category.category_name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_category(db=db, category=category)
