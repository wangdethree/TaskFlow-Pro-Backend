from fastapi import FastAPI
from .api.v1.health import router
from .core.config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("TaskFlow Pro 启动")

    yield

    print("TaskFlow Pro 关闭")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(
    router=router,
    prefix="/api/v1",
)
