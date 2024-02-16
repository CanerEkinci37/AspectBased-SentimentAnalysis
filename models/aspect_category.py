from sqlalchemy import Column, ForeignKey, SmallInteger, String

from ..app.database import Base


class AspectCategory(Base):
    __tablename__ = "aspect_categories"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, unique=True, index=True)
    business_category_id = Column(SmallInteger, ForeignKey("business_categories.id"))
