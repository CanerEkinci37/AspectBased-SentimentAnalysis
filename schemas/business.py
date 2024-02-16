from pydantic import BaseModel


class BusinessBase(BaseModel):
    name: str


class BusinessCreate(BusinessBase):
    pass


class Business(BusinessBase):
    id: int
    business_category_id: int

    class Config:
        orm_mode = True
