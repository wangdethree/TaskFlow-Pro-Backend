from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# 项目根目录
#
# 当前文件位置：
# backend/app/core/config.py
#
# parent.parent.parent.parent:
# core -> app -> backend -> 项目根目录
#
# 用于定位 .env 文件的位置
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    """
    项目配置管理类。

    使用 pydantic-settings 从环境变量或者 .env 文件中读取配置。

    好处：
    1. 避免将敏感信息直接写入代码；
    2. 不同环境可以使用不同配置；
    3. pydantic 会自动进行类型校验。
    """

    # ==========================
    # 应用基础配置
    # ==========================

    # 应用名称
    app_name: str

    # 应用版本
    app_version: str

    # 是否开启调试模式
    #
    # 开发环境：
    # debug=True
    #
    # 生产环境：
    # debug=False
    debug: bool

    # 当前运行环境
    #
    # 例如：
    # development
    # test
    # production
    environment: str


    # ==========================
    # 数据库配置
    # ==========================

    # 数据库连接地址
    #
    # 示例：
    # mysql+asyncmy://user:password@host:port/database
    #
    # mysql:
    #   数据库类型
    #
    # asyncmy:
    #   异步MySQL驱动
    #
    # 后续SQLAlchemy会使用这个地址创建数据库连接。
    database_url: str


    # pydantic-settings配置
    model_config = SettingsConfigDict(

        # 指定读取环境变量的文件
        #
        # 项目启动时：
        # Settings会自动读取项目根目录下的.env文件。
        env_file=BASE_DIR / ".env",

        # .env文件编码
        env_file_encoding="utf-8",
    )


# 创建全局配置对象
#
# 项目其他地方直接：
#
# from app.core.config import settings
#
# 即可获取配置。
settings = Settings()