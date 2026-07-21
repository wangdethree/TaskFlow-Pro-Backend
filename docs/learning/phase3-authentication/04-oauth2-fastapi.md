> 主题：OAuth2 概念、FastAPI Bearer 依赖与认证链路。

# 背景

API 需要标准方式告诉客户端如何携带访问凭证。OAuth2 定义授权框架和多种授权流程，Bearer Token 定义“持有即可使用”的凭证语义。FastAPI 提供安全 Schema 与依赖，帮助描述和提取凭证。

项目使用相关组件并不等于已经实现完整第三方 OAuth2 授权服务器，需要准确区分协议范围。

# 核心思想

FastAPI 的 OAuth2 工具主要把认证要求纳入依赖图和 OpenAPI，并从 Authorization Header 提取 Token。真正的用户验证、Token 签发、撤销和权限仍由应用实现。

Bearer Token 没有持有者证明，泄露者即可使用，因此传输、存储、有效期和日志保护是安全边界的一部分。

# 工作原理

登录端点验证凭证并返回 Token。受保护请求携带 `Authorization: Bearer ...`，OAuth2 依赖提取字符串，Token Service 校验签名与声明，用户 Repository 获取主体，当前用户依赖检查账户状态。

安全 Scheme 会进入 OpenAPI，使交互文档知道登录地址与 Bearer 要求。它只描述契约，不替代服务端校验。

# 企业实践

- 凭证解析、Token 校验和用户加载拆成可组合依赖。
- 认证失败返回统一语义并设置合适认证头。
- 若未来支持第三方登录，应采用适合公开客户端的授权码加 PKCE 等流程，而非复用密码登录接口。
- Scope 只在有明确授权模型时采用，不把它当作项目数据权限替代品。
- 文档环境也不能暴露真实长期 Token。
- 测试覆盖缺失、格式错误、过期和主体无效的 Token。

# TaskFlow Pro应用

FastAPI OAuth2PasswordBearer 可用于声明 Bearer 提取和登录入口；TaskFlow 自己的认证 Service 负责邮箱密码验证和 JWT 签发。

`get_current_user` 得到用户后，RBAC 和项目成员判断继续执行。未来 Agent Tool 若非 HTTP 调用，应接收已经建立的授权上下文，不强行复用 Header 解析。

# 常见误区

- 认为使用 OAuth2PasswordBearer 就完成 OAuth2 协议。
- 把认证 Scheme 当作 JWT 验证器。
- Scope 与项目角色重复建模却没有一致性方案。
- 在查询参数中传递 Token，增加日志泄露。
- 只测试 Swagger 授权按钮，不测试异常凭证。

# 学习检查问题

1. OAuth2、Bearer Token 和 JWT 是什么关系？
2. FastAPI Security Scheme 实际完成哪些工作？
3. Token 字符串提取后还需要哪些验证步骤？
4. Scope 为什么不能自动表达“某项目的 Manager”？
5. 非 HTTP Agent Tool 怎样复用认证后的身份？
