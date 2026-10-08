from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI

import app.models
from app.db.database import Base, engine
from app.routers import auth, housing, user
from ml.config import MODEL_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load(MODEL_PATH)
    yield


app = FastAPI(title="Housing App", lifespan=lifespan)
Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(housing.router)
app.include_router(user.router)
