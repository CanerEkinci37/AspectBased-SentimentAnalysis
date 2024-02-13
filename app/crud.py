from sqlalchemy.orm import Session
from . import models, schemas

# RESTAURANT


def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).offset(skip).limit(limit=limit).all()


def get_restaurant_by_name(db: Session, restaurant_name: str):
    return (
        db.query(models.Restaurant)
        .filter(models.Restaurant.restaurant_name.ilike(restaurant_name))
        .all()
    )


def create_restaurant(
    db: Session,
    restaurant_name: str,
    category_count: int,
    category_id: int,
):
    db_restaurant = models.Restaurant(
        restaurant_name=restaurant_name,
        category_count=category_count,
        restaurant_category_id=category_id,
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


# RESTAURANT CATEGORY


def create_restaurant_category(db: Session, category: schemas.RestaurantCategoryCreate):
    db_category = models.RestaurantCategory(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_restaurant_category_by_name(db: Session, category_name: str):
    row = (
        db.query(models.RestaurantCategory)
        .filter(models.RestaurantCategory.category_name.ilike(category_name))
        .first()
    )
    if row:
        return row
    return None


# OTEL


def get_otels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Otel).offset(skip).limit(limit=limit).all()


def get_otel_by_name(db: Session, otel_name: str):
    return db.query(models.Otel).filter(models.Otel.otel_name.ilike(otel_name)).all()


def create_otel(
    db: Session,
    otel_name: str,
    category_count: int,
    category_id: int,
):
    db_otel = models.Otel(
        otel_name=otel_name,
        category_count=category_count,
        otel_category_id=category_id,
    )
    db.add(db_otel)
    db.commit()
    db.refresh(db_otel)
    return db_otel


# OTEL CATEGORY


def get_otel_category_by_name(db: Session, category_name: str):
    row = (
        db.query(models.OtelCategory)
        .filter(models.OtelCategory.category_name.ilike(category_name))
        .first()
    )
    if row:
        return row
    return None


def create_otel_category(db: Session, category: schemas.OtelCategoryCreate):
    db_category = models.OtelCategory(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
