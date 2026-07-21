from fastapi import FastAPI
from .api.v1.health import router

app = FastAPI(
    title="TaskFlow Pro API",
    version="0.1.0",
)

app.include_router(
    router=router,
    prefix="/api/v1",
)
