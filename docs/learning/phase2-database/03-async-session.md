> 主题：AsyncEngine、连接池、AsyncSession 与请求级生命周期。

# 背景

FastAPI 能在数据库 I/O 等待时处理其他请求，但前提是数据库驱动和调用链真正支持异步。共享全局 Session 或忘记关闭连接，会导致并发状态污染和连接池耗尽。

AsyncSession 的学习重点不是把方法前加 `await`，而是理解连接、事务和 ORM 状态在并发请求中的边界。

# 核心思想

Engine 管理方言和连接池，Session 管理一个工作单元中的 ORM 状态与事务。Session 是有状态对象，不应跨并发任务共享。

常见 Web 模式是一请求一个 AsyncSession，通过依赖获取并确保关闭；Service 在用例边界决定提交或回滚。

# 工作原理

AsyncEngine 通过异步驱动与数据库通信，连接池复用物理连接。创建 Session 不一定立即取出连接，首次需要数据库 I/O 时才从池中获取。

`await session.execute(...)` 等操作把控制权交回事件循环，等待驱动完成网络 I/O。事务结束后连接归还池，Session 关闭后清理其资源与对象关联。

AsyncSession 不能安全地被多个并发 Task 同时使用，因为 identity map、事务和连接状态会互相影响。每个并发工作单元应使用独立 Session。

# 企业实践

- 使用 `async_sessionmaker` 统一 Session 配置。
- 通过 `yield` 依赖保证请求结束时关闭 Session。
- 对连接池大小、等待超时和回收策略进行容量设计。
- 异常时显式回滚，使 Session 恢复可用状态。
- 禁止在响应序列化期间触发未计划的数据库 I/O。
- Celery 任务自行创建独立 Session，不能复用请求 Session。

# TaskFlow Pro应用

每个 API 请求注入一个 AsyncSession。Service 完成创建项目与添加创建者成员等多步操作后统一提交；任一步骤失败则整体回滚。

后台通知、统计和 Agent 异步任务拥有各自 Session 生命周期。连接池参数需结合 Uvicorn Worker、Celery 并发和 MySQL 上限共同计算。

# 常见误区

- 把 AsyncSession 定义成全局单例。
- 认为创建 Session 就永久占用一条连接。
- Repository 每执行一次 SQL 就 commit。
- 异常后继续使用未回滚的 Session。
- 在多个 `asyncio` Task 中共享同一 Session。

# 学习检查问题

1. Engine、连接池、连接和 Session 的关系是什么？
2. 为什么 Session 不能跨并发请求共享？
3. `yield` 依赖如何保证资源释放？
4. Uvicorn 与 Celery 并发如何共同影响连接池容量？
5. 异常后为什么通常需要 rollback？
