from sqlalchemy.orm import Session

from . import models, schemas


def get_restaurant(db: Session, restaurant_id: int):
    return (
        db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).all()
    )


def get_restaurant_by_name(db: Session, restaurant_name: str):
    return (
        db.query(models.Restaurant)
        .filter(models.Restaurant.restaurant_name == restaurant_name)
        .all()
    )


def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).offset(skip).limit(limit=limit).all()


def create_restaurant(
    db: Session,
    restaurant_name: str,
    category_count: int,
    category_id: int,
):
    db_restaurant = models.Restaurant(
        restaurant_name=restaurant_name,
        category_count=category_count,
        category_id=category_id,
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit=limit).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category_id_by_name(db: Session, category_name: str):
    category_row = (
        db.query(models.Category)
        .filter(models.Category.category_name == category_name)
        .first()
    )
    if category_row:
        return category_row.id
    return None
