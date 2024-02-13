from fastapi import Depends, FastAPI
from . import models, database
from .routers import restaurant_categories, restaurants, otel_categories, otels

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(restaurant_categories.router)
app.include_router(otel_categories.router)
app.include_router(restaurants.router)
app.include_router(otels.router)
