from pydantic import BaseModel


class SentimentCategoryBase(BaseModel):
    name: str


class SentimentCategoryCreate(SentimentCategoryBase):
    pass


class SentimentCategory(SentimentCategoryBase):
    id: int

    class Config:
        orm_mode = True
