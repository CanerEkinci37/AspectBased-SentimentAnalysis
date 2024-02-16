from pydantic import BaseModel


class AspectSentimentCategoryBase(BaseModel):
    pass


class AspectSentimentCategoryCreate(AspectSentimentCategoryBase):
    pass


class AspectSentimentCategory(AspectSentimentCategoryBase):
    id: int
    aspect_category_id: int
    sentiment_id: int

    class Config:
        orm_mode = True
