from fastapi import FastAPI

from . import models
from .routers import categories, businesses, index
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(index.router)
app.include_router(categories.router)
app.include_router(businesses.router)
