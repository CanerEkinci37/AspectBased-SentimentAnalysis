from sqlalchemy.orm import Session

from . import models, schemas


# Business Category


def get_distinct_business_category_names(db: Session):
    business_categories = db.query(models.BusinessCategory.name.distinct()).all()
    return business_categories


def get_business_category_name(db: Session, id: int):
    business_category = (
        db.query(models.BusinessCategory)
        .filter(models.BusinessCategory.id == id)
        .first()
    )
    return business_category.name


def get_business_category_id(db: Session, name: str):
    business_category = (
        db.query(models.BusinessCategory)
        .filter(models.BusinessCategory.name.ilike(name))
        .first()
    )

    if business_category:
        return business_category.id


def create_business_category(
    db: Session, business_category: schemas.BusinessCategoryCreate
):
    db_business_category = models.BusinessCategory(**business_category.dict())
    db.add(db_business_category)
    db.commit()
    db.refresh(db_business_category)
    return db_business_category


# Sentiment Category


def get_sentiment_category_by_id(db: Session, id: int):
    sentiment_category = (
        db.query(models.SentimentCategory)
        .filter(models.SentimentCategory.id == id)
        .first()
    )
    return sentiment_category


def get_sentiment_category_id(db: Session, name: str):
    sentiment_category = (
        db.query(models.SentimentCategory)
        .filter(models.SentimentCategory.name.ilike(name))
        .first()
    )

    if sentiment_category:
        return sentiment_category.id


def create_sentiment_category(
    db: Session, sentiment_category: schemas.SentimentCategoryCreate
):
    db_sentiment_category = models.SentimentCategory(**sentiment_category.dict())
    db.add(db_sentiment_category)
    db.commit()
    db.refresh(db_sentiment_category)
    return db_sentiment_category


# Aspect Category


def get_aspect_category_by_id(db: Session, id: int):
    aspect_category = (
        db.query(models.AspectCategory).filter(models.AspectCategory.id == id).first()
    )
    return aspect_category


def get_aspect_category_id(db: Session, name: str, business_category_id: int):
    aspect_category = (
        db.query(models.AspectCategory)
        .filter(
            models.AspectCategory.name.ilike(name),
            models.AspectCategory.business_category_id == business_category_id,
        )
        .first()
    )

    if aspect_category:
        return aspect_category.id


def create_aspect_category(
    db: Session,
    aspect_category: schemas.AspectCategoryCreate,
    business_category_id: int,
):
    db_aspect_category = models.AspectCategory(
        **aspect_category.dict(), business_category_id=business_category_id
    )
    db.add(db_aspect_category)
    db.commit()
    db.refresh(db_aspect_category)
    return db_aspect_category


# Business


def get_distinct_business_names(db: Session):
    businesses = db.query(models.Business.name.distinct()).all()
    return businesses


def get_businesses(db: Session):
    businesses = db.query(
        models.Business.name, models.Business.business_category_id
    ).all()
    return businesses


def get_business_id(db: Session, name: str, business_category_id: int):
    db_business = (
        db.query(models.Business)
        .filter(
            models.Business.name.ilike(name),
            models.Business.business_category_id == business_category_id,
        )
        .first()
    )
    if db_business:
        return db_business.id


def create_business(db: Session, business_name: str, business_category_id):
    db_business = models.Business(
        name=business_name, business_category_id=business_category_id
    )
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


# Aspect Sentiment Category


def get_aspect_sentiment_category_by_id(db: Session, id: int):
    aspect_sentiment_category = (
        db.query(models.AspectSentimentCategory)
        .filter(models.AspectSentimentCategory.id == id)
        .first()
    )
    return aspect_sentiment_category


def get_aspect_sentiment_category_id(
    db: Session, sentiment_id: int, aspect_category_id: int
):
    aspect_sentiment_category = (
        db.query(models.AspectSentimentCategory)
        .filter(
            models.AspectSentimentCategory.sentiment_id == sentiment_id,
            models.AspectSentimentCategory.aspect_category_id == aspect_category_id,
        )
        .first()
    )
    if aspect_sentiment_category:
        return aspect_sentiment_category.id


def create_aspect_sentiment(db: Session, aspect_category_id: int, sentiment_id: int):
    db_aspect_sentiment = models.AspectSentimentCategory(
        aspect_category_id=aspect_category_id, sentiment_id=sentiment_id
    )
    db.add(db_aspect_sentiment)
    db.commit()
    db.refresh(db_aspect_sentiment)
    return db_aspect_sentiment


# Business Record


def get_business_records_by_business(db: Session, business_id: int):
    record = (
        db.query(models.BusinessRecord)
        .filter(models.BusinessRecord.business_id == business_id)
        .all()
    )
    return record


def get_business_record(
    db: Session, business_id: int, aspect_sentiment_category_id: int
):
    db_business_record = (
        db.query(models.BusinessRecord)
        .filter(
            models.BusinessRecord.business_id == business_id,
            models.BusinessRecord.aspect_sentiment_category_id
            == aspect_sentiment_category_id,
        )
        .first()
    )
    return db_business_record


def create_business_record(
    db: Session, business_id: int, aspect_sentiment_category_id: int, count: int
):
    db_business_record = models.BusinessRecord(
        business_id=business_id,
        aspect_sentiment_category_id=aspect_sentiment_category_id,
        count=count,
    )
    db.add(db_business_record)
    db.commit()
    db.refresh(db_business_record)
    return db_business_record


def get_business_records_by_name_and_category(
    db: Session, business_name: str, category_name: str
):
    category_id = get_business_category_id(db=db, name=category_name)
    business_id = get_business_id(
        db=db, name=business_name, business_category_id=category_id
    )
    records = get_business_records_by_business(db=db, business_id=business_id)
    return records


def get_aspect_sentiment_by_record(db, record: models.BusinessRecord):
    db_aspect_sentiment = get_aspect_sentiment_category_by_id(
        db=db, id=record.aspect_sentiment_category_id
    )
    if db_aspect_sentiment:
        print(db_aspect_sentiment.aspect_category_id)
    db_aspect = get_aspect_category_by_id(
        db=db, id=db_aspect_sentiment.aspect_category_id
    )
    db_sentiment = get_sentiment_category_by_id(
        db=db, id=db_aspect_sentiment.sentiment_id
    )
    return db_aspect.name.upper(), db_sentiment.name.upper()
