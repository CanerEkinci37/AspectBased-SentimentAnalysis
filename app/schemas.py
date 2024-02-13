from pydantic import BaseModel


class RestaurantBase(BaseModel):
    restaurant_name: str


class Restaurant(RestaurantBase):
    id: int
    category_count: int
    restaurant_category_id: int

    class Config:
        orm_mode = True


class RestaurantCategoryBase(BaseModel):
    category_name: str


class RestaurantCategoryCreate(RestaurantCategoryBase):
    pass


class RestaurantCategory(RestaurantCategoryBase):
    id: int

    class Config:
        orm_mode = True


class OtelBase(BaseModel):
    otel_name: str


class Otel(OtelBase):
    id: int
    category_count: int
    otel_category_id: int

    class Config:
        orm_mode = True


class OtelCategoryBase(BaseModel):
    category_name: str


class OtelCategoryCreate(OtelCategoryBase):
    pass


class OtelCategory(OtelCategoryBase):
    id: int

    class Config:
        orm_mode = True
