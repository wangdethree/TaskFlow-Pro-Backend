from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

# 创建异步数据库引擎
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)