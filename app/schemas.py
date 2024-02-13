from pydantic import BaseModel


class RestaurantBase(BaseModel):
    restaurant_name: str


class Restaurant(RestaurantBase):
    id: int
    category_count: int
    category_id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    category_name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
