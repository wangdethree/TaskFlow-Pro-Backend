# TaskFlow Pro Backend 学习知识库

## 这是什么

本目录是 TaskFlow Pro Backend 的长期工程知识库。它不承担“从第一页顺序讲完一门课程”的职责，而是为项目开发、故障排查、架构复盘和面试前回顾提供按主题检索的资料。

每篇文档重点回答七类问题：技术为什么出现、核心思想是什么、内部怎样工作、企业如何使用、在 TaskFlow Pro 中如何落地、常见误区有哪些，以及如何检查自己是否真正理解。

知识库不会罗列大量 API，也不会用面试结论代替工程推理。阅读目标是能够根据业务场景做选择，并解释设计的收益、成本和边界。

## 如何使用

不建议从头到尾连续阅读。更有效的方式是根据当前开发任务定位相关阶段：

1. 开发前先阅读该主题的“背景、核心思想和工作原理”。
2. 设计时重点查看“企业实践”和“TaskFlow Pro应用”。
3. Code Review 或排错时对照“常见误区”。
4. 模块完成后回答“学习检查问题”，暴露没有真正理解的部分。
5. 项目演进后同步更新对应文档，使知识库描述真实实现而不是理想模板。

这套资料是导航和决策依据，不替代官方文档、源码、测试和真实运行结果。涉及具体版本行为时，应以项目锁定版本的官方资料与测试为准。

## 按开发任务查询

| 当前任务 | 建议查阅 |
|---|---|
| 调整目录、导入或开发环境 | [`phase0-python-engineering/`](phase0-python-engineering/) |
| 设计 HTTP API、路由、Schema 或依赖 | [`phase1-fastapi/`](phase1-fastapi/) |
| 建表、编写查询、迁移或处理事务 | [`phase2-database/`](phase2-database/) |
| 开发注册、登录、密码和 Token | [`phase3-authentication/`](phase3-authentication/) |
| 设计角色、权限和项目数据范围 | [`phase4-rbac/`](phase4-rbac/) |
| 编写 Service、Repository 和任务状态流转 | [`phase5-business-development/`](phase5-business-development/) |
| 使用 Redis、Celery 或处理消息一致性 | [`phase6-cache-and-message/`](phase6-cache-and-message/) |
| 编写测试、日志或部署服务 | [`phase7-testing-and-deployment/`](phase7-testing-and-deployment/) |
| 开发 Agent、Tool Calling 和 AI 安全能力 | [`phase8-agent-extension/`](phase8-agent-extension/) |

## 阶段与 TaskFlow Pro 能力

### Phase 0：Python 工程基础

建立稳定的项目结构、解释器认知、虚拟环境和可复现依赖，为所有后续开发提供统一运行基础。

- [项目结构](phase0-python-engineering/01-project-structure.md)
- [虚拟环境](phase0-python-engineering/02-virtual-environment.md)
- [依赖管理](phase0-python-engineering/03-dependency-management.md)
- [Python 运行时](phase0-python-engineering/04-python-runtime.md)

### Phase 1：FastAPI

建立 HTTP 边界、ASGI 请求链路、模块化路由、Pydantic 数据边界和依赖注入体系。

- [HTTP 与 REST API](phase1-fastapi/01-http-rest-api.md)
- [FastAPI 核心机制](phase1-fastapi/02-fastapi-core.md)
- [Router](phase1-fastapi/03-router.md)
- [Pydantic](phase1-fastapi/04-pydantic.md)
- [依赖注入](phase1-fastapi/05-dependency-injection.md)

### Phase 2：数据库

建立关系模型、ORM、异步 Session、迁移和事务能力，保证核心业务数据正确演进。

- [MySQL 设计](phase2-database/01-mysql-design.md)
- [SQLAlchemy 2.0](phase2-database/02-sqlalchemy2.md)
- [AsyncSession](phase2-database/03-async-session.md)
- [Alembic](phase2-database/04-alembic.md)
- [事务](phase2-database/05-transaction.md)

### Phase 3：认证

建立可信身份边界，覆盖密码存储、JWT、Token 生命周期和 FastAPI OAuth2 认证链路。

- [认证基础](phase3-authentication/01-authentication-basic.md)
- [密码安全](phase3-authentication/02-password-security.md)
- [JWT](phase3-authentication/03-jwt.md)
- [FastAPI OAuth2](phase3-authentication/04-oauth2-fastapi.md)

### Phase 4：RBAC

建立角色权限模型，并把“能做什么”与“能操作哪些项目数据”同时纳入授权。

- [RBAC 模型](phase4-rbac/01-rbac-model.md)
- [权限设计](phase4-rbac/02-permission-design.md)
- [数据权限](phase4-rbac/03-data-permission.md)

### Phase 5：业务开发

建立业务编排、数据访问、领域建模、状态机和事务边界，避免系统退化为路由层 CRUD。

- [Service Layer](phase5-business-development/01-service-layer.md)
- [Repository Pattern](phase5-business-development/02-repository-pattern.md)
- [Domain Model](phase5-business-development/03-domain-model.md)
- [状态机](phase5-business-development/04-state-machine.md)
- [事务边界](phase5-business-development/05-transaction-boundary.md)

### Phase 6：缓存与消息

建立 Redis 缓存、Celery 后台任务和数据库—消息一致性能力，在性能与正确性之间做明确取舍。

- [Redis](phase6-cache-and-message/01-redis.md)
- [缓存设计](phase6-cache-and-message/02-cache-design.md)
- [Celery](phase6-cache-and-message/03-celery.md)
- [消息一致性](phase6-cache-and-message/04-message-consistency.md)

### Phase 7：测试与部署

建立可回归、可观测、可交付的工程体系，使服务能在干净环境稳定启动和排错。

- [pytest](phase7-testing-and-deployment/01-pytest.md)
- [测试策略](phase7-testing-and-deployment/02-testing-strategy.md)
- [Docker](phase7-testing-and-deployment/03-docker.md)
- [Docker Compose](phase7-testing-and-deployment/04-docker-compose.md)
- [Nginx](phase7-testing-and-deployment/05-nginx.md)
- [日志](phase7-testing-and-deployment/06-logging.md)

### Phase 8：Agent 扩展

在既有业务边界之上建立 Agent 和 Tool，保证 AI 调用仍经过权限、业务校验、审计和人工确认。

- [Agent 基础](phase8-agent-extension/01-agent-basic.md)
- [Tool Calling](phase8-agent-extension/02-tool-calling.md)
- [Agent 架构](phase8-agent-extension/03-agent-architecture.md)
- [Agent 安全](phase8-agent-extension/04-agent-security.md)
- [TaskFlow Agent 设计](phase8-agent-extension/05-taskflow-agent-design.md)

## 维护约定

- 文档描述应与当前代码和架构决策保持一致。
- 新增关键技术前，先说明它解决的真实问题与不采用它的后果。
- 版本相关细节注明适用范围，避免把短期实现写成永久真理。
- 示例聚焦决策与流程，不堆积可从官方文档直接查询的 API 列表。
- 重大设计变化应同步更新知识库、设计文档和测试。
- 已完成的早期学习笔记可以保留；本目录中的阶段资料作为长期主题索引。
