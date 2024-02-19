from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, dependencies, schemas

router = APIRouter()


@router.post("/create_business_category/", tags=["categories"])
async def create_business_category(
    business_category: schemas.BusinessCategoryCreate,
    db: Session = Depends(dependencies.get_db),
):
    id = crud.get_business_category_id(db=db, name=business_category.name)
    if id:
        raise HTTPException(
            status_code=400,
            detail=f"{business_category.name.title()} business category already exists",
        )
    return crud.create_business_category(db=db, business_category=business_category)


@router.post("/create_sentiment_category/", tags=["categories"])
async def create_sentiment_category(
    sentiment_category: schemas.SentimentCategoryCreate,
    db: Session = Depends(dependencies.get_db),
):
    id = crud.get_sentiment_category_id(db=db, name=sentiment_category.name)
    if id:
        raise HTTPException(
            status_code=400,
            detail=f"{sentiment_category.name.title()} sentiment category already exists",
        )
    return crud.create_sentiment_category(db=db, sentiment_category=sentiment_category)


@router.post("/create_aspect_category/", tags=["categories"])
async def create_aspect_category(
    aspect_category: schemas.AspectCategoryCreate,
    business_category_name: str,
    db: Session = Depends(dependencies.get_db),
):
    business_category_id = crud.get_business_category_id(
        db=db, name=business_category_name
    )
    if business_category_id:
        id = crud.get_aspect_category_id(
            db=db, name=aspect_category.name, business_category_id=business_category_id
        )
        if id:
            raise HTTPException(
                status_code=400,
                detail=f"{aspect_category.name.title()} aspect category already exists",
            )
        return crud.create_aspect_category(
            db=db,
            aspect_category=aspect_category,
            business_category_id=business_category_id,
        )
    raise HTTPException(
        status_code=404,
        detail=f"{business_category_name.title()} business category does not exists",
    )


@router.post("/create_aspect_sentiment_category/", tags=["categories"])
async def create_aspect_sentiment_category(
    business_category_name: str,
    aspect_category_name: str,
    sentiment_category_name: str,
    db: Session = Depends(dependencies.get_db),
):
    business_category_id = crud.get_business_category_id(
        db=db, name=business_category_name
    )
    if business_category_id:
        aspect_category_id = crud.get_aspect_category_id(
            db=db, name=aspect_category_name, business_category_id=business_category_id
        )
        if aspect_category_id:
            sentiment_category_id = crud.get_sentiment_category_id(
                db=db, name=sentiment_category_name
            )
            if sentiment_category_id:
                id = crud.get_aspect_sentiment_category_id(
                    db=db,
                    sentiment_id=sentiment_category_id,
                    aspect_category_id=aspect_category_id,
                )
                if id:
                    raise HTTPException(
                        status_code=400,
                        detail=f'{aspect_category_name.title() + " " + sentiment_category_name.title()} already exists for {business_category_name.title()}',
                    )
                return crud.create_aspect_sentiment(
                    db=db,
                    aspect_category_id=aspect_category_id,
                    sentiment_id=sentiment_category_id,
                )
            raise HTTPException(
                status_code=404,
                detail=f"{sentiment_category_name.title()} sentiment category does not exists",
            )
        raise HTTPException(
            status_code=404,
            detail=f"{aspect_category_name.title()} aspect category does not exists for {business_category_name.title()}",
        )
    raise HTTPException(
        status_code=404,
        detail=f"{business_category_name.title()} business category does not exists",
    )
