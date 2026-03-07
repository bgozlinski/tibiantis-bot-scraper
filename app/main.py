from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

http_client: httpx.AsyncClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client
    http_client = httpx.AsyncClient()
    yield
    await http_client.aclose()
app = FastAPI(lifespan=lifespan)

async def get_http_client():
    return http_client

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}