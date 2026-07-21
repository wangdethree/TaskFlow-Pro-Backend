> 主题：ORM 思想、SQLAlchemy 2.0 映射、查询与对象状态。

# 背景

手写 SQL 能精确控制数据库，但在大量实体、关系和重复映射中容易产生样板代码。ORM 用对象模型表达持久化，同时保留查询和事务能力。

ORM 不应让开发者忘记 SQL。企业使用它是为了统一映射、组合查询和管理对象状态，而不是假设数据库细节已经消失。

# 核心思想

SQLAlchemy 将 Core 的 SQL 表达能力与 ORM 的对象映射结合。2.0 风格强调显式 `select`、类型化声明和统一执行模型。

ORM Model 是持久化模型；Session 是工作单元和 identity map；Repository 封装用例需要的查询。性能与正确性仍取决于 SQL、关系加载和事务设计。

# 工作原理

Declarative Mapping 把 Python 类、列和关系绑定到 Table 元数据。查询表达式被编译为目标方言 SQL，经 Engine/Connection 发送到数据库，再把结果行组装为 ORM 对象。

Session 维护对象状态：transient、pending、persistent、deleted、detached。identity map 保证同一 Session 内同一主键通常对应同一 Python 对象。

flush 根据对象变化生成 SQL，但不等同于事务提交。关系加载可能在访问属性时发起额外查询；异步环境下隐式 I/O 更应被控制，通常采用显式预加载。

# 企业实践

- 使用 2.0 类型化声明，模型命名和数据库约束保持一致。
- Repository 返回业务需要的数据，不把通用“万能查询器”暴露给上层。
- 明确 eager loading，避免序列化阶段触发 N+1。
- 对批量统计等场景直接使用合适 SQL 表达式，而非加载所有对象计算。
- 开启查询日志用于开发排查，但生产日志需控制敏感参数与量。
- 不在 ORM Model 中混入 HTTP 响应职责。

# TaskFlow Pro应用

User、Project、ProjectMember、Task、Comment 等通过 Declarative Mapping 建模。项目详情需要成员和任务摘要时，应规划加载策略，不能在响应遍历中逐条触发查询。

Repository 使用 `select` 表达按项目、状态和负责人查询任务；Service 决定业务权限和事务，Schema 控制外部响应。

# 常见误区

- 认为 ORM 不需要理解 SQL 和索引。
- 把 `flush` 当作 `commit`。
- 返回 ORM 对象后关闭 Session，再访问未加载关系。
- 在循环中访问懒加载关系产生 N+1。
- 建立一个包含所有表操作的巨大 Repository。

# 学习检查问题

1. SQLAlchemy Core、ORM、Engine 和 Session 分别负责什么？
2. identity map 带来什么行为？
3. flush 与 commit 有什么区别？
4. 为什么异步环境更要避免隐式关系加载？
5. 哪些查询不适合把全部数据加载为 ORM 对象？
