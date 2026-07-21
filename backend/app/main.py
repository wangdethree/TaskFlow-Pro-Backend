from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.test_dependency import router as dependency_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("TaskFlow Pro 启动")

    yield

    print("TaskFlow Pro 关闭")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


app.include_router(
    health_router,
    prefix="/api/v1",
)


app.include_router(
    dependency_router,
    prefix="/api/v1",
)