> 主题：Agent 分层、控制器、工具注册、状态与异步执行。

# 背景

把 Prompt、模型 SDK、数据库查询和业务更新写在一个函数中，会让 Agent 无法测试、替换模型或复用权限。长任务还会阻塞 HTTP 请求。

Agent 架构需要把非确定推理与确定业务系统隔离，并为状态、执行、审计和失败建立边界。

# 核心思想

推荐依赖链为 `API/Job → Agent Orchestrator → Tool Registry → Tool Adapter → Service`。Orchestrator 管理循环和预算，Tool Adapter 做 Schema 与上下文适配，Service 保持业务权威。

模型供应商属于可替换基础设施，领域 Service 不应导入模型 SDK。对话状态、任务状态和业务数据采用不同存储生命周期。

# 工作原理

请求创建 Agent Run，Celery Worker 加载授权快照或可验证主体，Orchestrator 组装 Prompt 和允许工具，调用模型并执行工具循环。每步记录输入摘要、调用、观察和状态。

长任务状态通常经历 pending、running、succeeded、failed、cancelled。重试要复用 run/request ID，避免重复写入；恢复时从持久检查点而非内存继续。

# 企业实践

- 通过 Tool Registry 按角色和场景提供允许列表。
- 模型配置、Prompt 版本和 Tool 版本进入运行记录。
- Orchestrator 设置步数、Token、时间和并发预算。
- 读写路径分离，写入必须走确认状态机。
- 运行状态持久化，Web 只轮询或订阅结果。
- 模型替换用契约测试和评测集验证，不只比较主观文案。

# TaskFlow Pro应用

`app/agents/` 后续承载 Orchestrator 和场景定义，`app/tools/` 适配 ProjectService、TaskService、StatisticsService；`app/tasks/` 运行长 AI Job。

项目风险分析 Run 保存项目、发起用户、模型/Prompt 版本和报告状态。Tool 查询始终使用当前授权范围，Run 过久时还要重新确认敏感写权限。

# 常见误区

- Agent 模块直接导入 SQLAlchemy Session 执行查询。
- 把全部对话和业务状态只存在内存。
- HTTP 请求同步等待多轮模型调用。
- 所有用户获得完整 Tool Registry。
- 更换模型后不运行回归评测。

# 学习检查问题

1. Orchestrator、Tool Adapter 和 Service 分别负责什么？
2. 为什么模型 SDK 不应进入领域 Service？
3. 长 Agent Run 怎样与 HTTP 生命周期解耦？
4. Tool 允许列表如何根据用户和场景生成？
5. 哪些运行元数据必须持久化以支持复盘？
