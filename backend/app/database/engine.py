from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings


# 创建异步数据库引擎
#
# Engine 是 SQLAlchemy 连接数据库的核心对象。
#
# 它负责：
# 1. 管理数据库连接池；
# 2. 根据需要获取数据库连接；
# 3. 与 MySQL 数据库建立通信。
#
# 注意：
# Engine 本身不是一次数据库操作。
# 真正执行SQL的是后续创建的 Session。
engine: AsyncEngine = create_async_engine(
    settings.database_url,

    # 开发环境开启SQL日志，方便查看SQL执行情况。
    #
    # 生产环境通常关闭。
    echo=settings.debug,
)