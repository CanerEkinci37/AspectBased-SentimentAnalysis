from fastapi import Depends, FastAPI
from . import models, database
from .routers import categories, restaurants

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(categories.router)
app.include_router(restaurants.router)
