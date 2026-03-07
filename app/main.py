from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI
from app.routers import character
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient()
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(character.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
