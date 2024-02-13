from sqlalchemy import Column, SmallInteger, String, ForeignKey

from .database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(SmallInteger, primary_key=True)
    restaurant_name = Column(String)
    category_count = Column(SmallInteger)
    restaurant_category_id = Column(
        SmallInteger, ForeignKey("restaurant_categories.id")
    )


class RestaurantCategory(Base):
    __tablename__ = "restaurant_categories"

    id = Column(SmallInteger, primary_key=True)
    category_name = Column(String, unique=True, index=True)


class Otel(Base):
    __tablename__ = "otels"

    id = Column(SmallInteger, primary_key=True)
    otel_name = Column(String)
    category_count = Column(SmallInteger)
    otel_category_id = Column(SmallInteger, ForeignKey("otel_categories.id"))


class OtelCategory(Base):
    __tablename__ = "otel_categories"

    id = Column(SmallInteger, primary_key=True)
    category_name = Column(String)
