> 主题：Tool Calling、结构化 Schema、执行器与幂等写入。

# 背景

模型生成自然语言无法安全调用业务能力，字符串参数容易歧义，模型也可能发明不存在的项目或字段。Tool Calling 用明确名称和 Schema 将模型意图转换为可验证调用。

Tool 不是把数据库函数暴露给模型，而是面向业务的最小受控能力。

# 核心思想

模型只提出调用建议，应用运行时才是权威执行者。执行前必须验证参数、身份、权限、业务规则和确认状态。

Tool 设计应高内聚、最小权限、结果结构稳定。读工具与写工具分开，危险操作不使用模糊“万能执行”接口。

# 工作原理

系统向模型提供 Tool 名称、描述和 JSON Schema。模型返回名称与参数；执行器解析并校验，注入可信用户上下文，调用 Service，再把结构化结果或安全错误返回模型。

写 Tool 使用幂等键或请求 ID。模型可能重复调用或在重试中再次执行，执行器不能假设每个调用只发生一次。

# 企业实践

- 参数使用稳定 ID 和受控枚举，不让模型生成任意 SQL。
- Tool 描述明确前置条件、效果和限制。
- 返回最小必要字段并限制列表大小。
- 写操作区分“计划/预览”和“确认执行”。
- 对每次调用记录 Tool、用户、资源、结果和关联 ID。
- Tool 版本演进保持 Schema 兼容或显式版本化。

# TaskFlow Pro应用

`get_project_summary`、`list_overdue_tasks` 和 `get_member_load` 是只读工具；`propose_tasks` 只生成候选，`create_confirmed_tasks` 在用户确认后调用 TaskService。

Tool 层位于 Agent 与 Service 之间，注入当前用户但不允许模型自行填写操作者 ID。列表工具自动应用数据权限和分页上限。

# 常见误区

- 提供 `execute_sql` 或任意 HTTP Tool。
- 信任模型传入的 user_id。
- 写 Tool 没有幂等和确认。
- 返回整表数据给模型。
- Tool 捕获所有异常后伪造成功文本。

# 学习检查问题

1. 模型输出 Tool Call 后，运行时还要做哪些检查？
2. 为什么 Tool 应调用 Service 而非 Repository？
3. 预览与执行分离怎样降低写操作风险？
4. 重复 Tool Call 如何保持幂等？
5. 为什么任意 SQL Tool 不适合 TaskFlow？
