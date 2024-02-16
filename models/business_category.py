from sqlalchemy import Column, SmallInteger, String

from ..app.database import Base


class BusinessCategory(Base):
    __tablename__ = "business_categories"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, unique=True, index=True)
