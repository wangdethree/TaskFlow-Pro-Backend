> 主题：Service Layer、业务用例编排与跨入口复用。

# 背景

当路由直接查询数据库并判断权限时，HTTP、业务和持久化耦合。Celery 或 Agent Tool 想执行相同用例只能复制逻辑，最终出现规则不一致。

Service Layer 为应用用例建立统一入口，使业务行为不依赖具体传输协议。

# 核心思想

Service 以业务动作组织代码，例如创建项目、分配任务、完成任务，而不是简单包装每张表的 CRUD。它编排 Repository、权限策略、事务和领域规则。

Service 返回业务结果或业务错误，API 再映射为 HTTP 响应。这样同一 Service 可以被 API、命令、后台任务和 Tool 调用。

# 工作原理

一次用例进入 Service 后，先建立主体和输入上下文，加载必要资源，执行授权和不变量校验，在事务内调用 Repository 写入，最后产生结果或待处理事件。

Service 可以依赖接口化的 Repository 和基础设施端口，测试时用替代实现隔离数据库；但过度 Mock 会掩盖真实查询与事务问题，需要配合集成测试。

# 企业实践

- 方法命名表达用例而非表操作。
- 事务边界围绕完整用例，Repository 不自行 commit。
- 业务异常使用稳定类型，避免泄露数据库异常。
- 不把 FastAPI Request/Response 传入核心 Service。
- 控制 Service 大小，按业务模块拆分而不是建立万能服务。
- 外部通知在提交后处理，并考虑可靠投递。

# TaskFlow Pro应用

ProjectService 负责创建项目并添加创建者成员；TaskService 负责验证成员、分配负责人和状态流转；CommentService 负责评论所有权规则。

未来 `create_task` Tool 与 HTTP 创建任务端点调用同一 TaskService，确保 Agent 不能绕过负责人合法性和项目权限。

# 常见误区

- Service 只有一行 Repository 转发却没有语义。
- Service 接收 HTTP Request 并直接返回状态码。
- 一个 ApplicationService 包含所有业务模块。
- 业务规则在 API、Service 和 Celery 各复制一份。
- 在数据库提交前发送不可撤销外部消息。

# 学习检查问题

1. Service 为什么按用例而不是按表 CRUD 组织？
2. API 与 Service 的错误边界如何转换？
3. 创建项目的事务应包含哪些操作？
4. 为什么 Tool 复用 Service 比复用 Router 更合理？
5. 什么样的 Service 抽象属于机械转发？
