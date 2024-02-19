from sqlalchemy import Column, ForeignKey, SmallInteger, String

from .database import Base


class BusinessCategory(Base):
    __tablename__ = "business_categories"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, unique=True, index=True)


class SentimentCategory(Base):
    __tablename__ = "sentiment_categories"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, unique=True, index=True)


class AspectCategory(Base):
    __tablename__ = "aspect_categories"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, index=True)
    business_category_id = Column(SmallInteger, ForeignKey("business_categories.id"))


class Business(Base):
    __tablename__ = "businesses"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, index=True)
    business_category_id = Column(SmallInteger, ForeignKey("business_categories.id"))


class AspectSentimentCategory(Base):
    __tablename__ = "aspect_sentiment_categories"

    id = Column(SmallInteger, primary_key=True)
    aspect_category_id = Column(
        SmallInteger, ForeignKey("aspect_categories.id"), index=True
    )
    sentiment_id = Column(
        SmallInteger, ForeignKey("sentiment_categories.id"), index=True
    )


class BusinessRecord(Base):
    __tablename__ = "business_records"

    id = Column(SmallInteger, primary_key=True)
    count = Column(SmallInteger)
    business_id = Column(SmallInteger, ForeignKey("businesses.id"))
    aspect_sentiment_category_id = Column(
        SmallInteger, ForeignKey("aspect_sentiment_categories.id"), index=True
    )
