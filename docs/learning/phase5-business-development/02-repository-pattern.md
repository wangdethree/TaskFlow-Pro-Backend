> 主题：Repository Pattern、查询封装与持久化边界。

# 背景

业务代码直接散布 ORM 查询后，表结构、加载策略和分页细节会渗透到所有 Service。查询优化或替换存储方式时影响范围扩大，测试也难以控制数据访问。

Repository 把领域需要的集合式访问与具体持久化实现分离。

# 核心思想

Repository 不是为 ORM 每个方法再包一层，而是提供业务需要的查询语言，例如“查找用户可见项目”“获取带成员的任务”。

它负责数据访问，不负责决定调用者是否有业务权限。授权条件可作为明确参数或专用查询的一部分，但策略由上层定义。

# 工作原理

Repository 接收 Session，构造 SQLAlchemy `select`、关联、过滤和加载策略，执行后返回实体或查询结果。写入时把对象加入当前工作单元，flush 获取数据库生成值，但通常不提交事务。

专用查询能集中处理分页、排序、N+1 和作用域过滤。通用 Repository 若暴露任意字段查询，反而会把数据库结构重新泄露给 Service。

# 企业实践

- 接口围绕业务查询命名，不建立万能 `filter_by(**kwargs)`。
- 明确返回单个、可选、列表或分页结果的语义。
- Repository 集成测试使用真实数据库行为验证约束与查询。
- 加载策略由用例决定，避免全局 eager 或隐式 lazy。
- 不在 Repository 捕获所有异常并返回 `None`。
- 批量更新要考虑 ORM 状态同步与审计需求。

# TaskFlow Pro应用

UserRepository 提供按规范化邮箱查找；ProjectRepository 查询用户参与项目；TaskRepository 按项目、状态、负责人分页并验证父子关系。

Service 注入当前 Session 下的 Repository，在一个事务中组合多次访问。Agent Tool 不直接持有 Repository，以免绕过权限和业务规则。

# 常见误区

- Repository 只是 ORM Session 的同名方法集合。
- 在每个写方法中 commit。
- 返回数据库异常字符串给 API。
- 用一个 BaseRepository 解决所有复杂查询。
- 为了“可替换数据库”设计从未需要的抽象层。

# 学习检查问题

1. Repository 与 ORM Session 的职责有何不同？
2. 为什么 Repository 通常不提交事务？
3. 哪类查询值得成为专用 Repository 方法？
4. 数据范围过滤进入查询是否意味着 Repository 负责授权？
5. 如何测试 Repository 才不会只验证 Mock 行为？
