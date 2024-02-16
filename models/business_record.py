from sqlalchemy import Column, ForeignKey, SmallInteger

from ..app.database import Base


class BusinessRecord(Base):
    __tablename__ = "business_records"

    id = Column(SmallInteger, primary_key=True)
    business_id = Column(SmallInteger, ForeignKey("businesses.id"))
    aspect_sentiment_category_id = Column(
        SmallInteger, ForeignKey("aspect_sentiment_categories.id")
    )
    count = Column(SmallInteger)
