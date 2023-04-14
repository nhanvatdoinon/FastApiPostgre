from fastapi import FastAPI
from .database import SessionLocal, engine
from . import  models
from .routes import route

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(route)

# Dependency

