from sqlalchemy import Column, ForeignKey, SmallInteger, String

from ..app.database import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, index=True)
    business_category_id = Column(SmallInteger, ForeignKey("business_categories.id"))
