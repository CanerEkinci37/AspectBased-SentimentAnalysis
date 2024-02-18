from pydantic import BaseModel


class BusinessCategoryBase(BaseModel):
    name: str


class BusinessCategoryCreate(BusinessCategoryBase):
    pass


class BusinessCategory(BusinessCategoryBase):
    id: int

    class Config:
        orm_mode = True


class SentimentCategoryBase(BaseModel):
    name: str


class SentimentCategoryCreate(SentimentCategoryBase):
    pass


class SentimentCategory(SentimentCategoryBase):
    id: int

    class Config:
        orm_mode = True


class AspectCategoryBase(BaseModel):
    name: str


class AspectCategoryCreate(AspectCategoryBase):
    pass


class AspectCategory(AspectCategoryBase):
    id: int
    business_category_id: int

    class Config:
        orm_mode = True


class BusinessBase(BaseModel):
    name: str


class BusinessCreate(BusinessBase):
    pass


class Business(BusinessBase):
    id: int
    business_category_id: int

    class Config:
        orm_mode = True


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
