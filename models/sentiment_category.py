from sqlalchemy import Column, SmallInteger, String

from ..app.database import Base


class SentimentCategory(Base):
    __tablename__ = "sentiment_categories"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, unique=True, index=True)
