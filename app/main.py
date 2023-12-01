from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.endpoints import weather
from app.api.v1.endpoints.login import login_router

from fastapi.middleware.cors import CORSMiddleware
from app.db.mongo_client import MongoDB
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    MongoDB.initialize()
    yield
    MongoDB.close()


app = FastAPI(title="Weather Forecast API")
app.include_router(login_router, prefix="/auth", tags=["Login"])
app.include_router(weather.router, prefix="/weather", tags=["weather"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
