from pydantic import BaseModel


class AspectCategoryBase(BaseModel):
    name: str


class AspectCategoryCreate(AspectCategoryBase):
    pass


class AspectCategory(AspectCategoryBase):
    id: int
    business_category_id: int

    class Config:
        orm_mode = True
