from pydantic import BaseModel


class BusinessCategoryBase(BaseModel):
    name: str


class BusinessCategoryCreate(BusinessCategoryBase):
    pass


class BusinessCategory(BusinessCategoryBase):
    id: int

    class Config:
        orm_mode = True
