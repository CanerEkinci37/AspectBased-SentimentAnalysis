from pydantic import BaseModel


class BusinessRecordBase(BaseModel):
    count: str


class BusinessRecordCreate(BusinessRecordBase):
    pass


class BusinessRecord(BusinessRecordBase):
    id: int
    business_id: int
    aspect_sentiment_category_id: int

    class Config:
        orm_mode = True
