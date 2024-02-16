from sqlalchemy import Column, ForeignKey, SmallInteger

from ..app.database import Base


class AspectSentimentCategory(Base):
    __tablename__ = "aspect_sentiment_categories"

    id = Column(SmallInteger, primary_key=True)
    aspect_category_id = Column(
        SmallInteger, ForeignKey("aspect_categories.id"), index=True
    )
    sentiment_id = Column(
        SmallInteger, ForeignKey("sentiment_categories.id"), index=True
    )
