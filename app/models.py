from sqlalchemy import Column, SmallInteger, String, ForeignKey

from .database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(SmallInteger, primary_key=True)
    restaurant_name = Column(String)
    category_count = Column(SmallInteger)
    category_id = Column(SmallInteger, ForeignKey("categories.id"))


class Category(Base):
    __tablename__ = "categories"
    id = Column(SmallInteger, primary_key=True)
    category_name = Column(String, unique=True, index=True)
