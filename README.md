# GL DevOps Platform

一个面向中小团队的运维平台，聚焦三类核心能力：

- `Portal`：统一首页，展示资产、域名、账单、任务和告警概览
- `Domain Management`：同步阿里云、Cloudflare 域名与解析记录，并对记录进行批量治理
- `Server Management`：同步阿里云、AWS 云服务器，并进一步同步到 JumpServer
- `Billing Analysis`：拉取阿里云、AWS 账单，基于标签维度做成本分析

当前仓库先按三个阶段推进：

1. 功能规划
2. 开发计划
3. 分阶段实施

## 技术选型

- 后端：`Python + Django + Django REST Framework`
- 管理后台：`Django Admin + Unfold`，用于配置和运营管理
- 数据库：`MySQL`
- 缓存和消息：`Redis`
- 异步与定时任务：`Celery + Celery Beat`
- 前端：`Vue + Tailwind CSS`
- 架构：前后端分离

## 设计原则

- `Django REST Framework` 负责提供前后端分离 API
- 主要业务流程和交互页面放在 `Vue` 前端实现
- `Django Admin` 主要承担账号配置、规则配置、任务运营、审计查看等后台能力
- Admin 主题方案固定为 `Unfold`
- `Django Admin` 需要基于 `Unfold` 做品牌化和体验优化，避免默认后台风格直接上线

## 推荐模块

- `portal`：首页看板、待办、任务状态、统计图表
- `domain`：域名、DNS 记录、同步任务、批量操作
- `asset`：云账号、区域、主机、标签、资产生命周期
- `jumpserver`：资产推送、变更检测、同步日志
- `billing`：账单拉取、费用明细、标签归集、报表分析
- `scheduler`：定时任务、重试、任务审计
- `auth`：用户、角色、权限、审计日志

## 先做什么

建议按下面顺序推进 MVP：

1. 云账号接入与凭证管理
2. 域名与 DNS 记录同步
3. ECS/EC2 资产同步
4. JumpServer 资产推送
5. 阿里云/AWS 账单采集
6. 基于标签的成本分析与首页展示

## 文档

- [feature-plan.md](/Users/guoqingao/workspace/golang/src/gitlab/gl-devops/docs/feature-plan.md)
- [development-plan.md](/Users/guoqingao/workspace/golang/src/gitlab/gl-devops/docs/development-plan.md)
- [platform-design.md](/Users/guoqingao/workspace/golang/src/gitlab/gl-devops/docs/platform-design.md)
- [module-list.md](/Users/guoqingao/workspace/golang/src/gitlab/gl-devops/docs/module-list.md)
- [page-list.md](/Users/guoqingao/workspace/golang/src/gitlab/gl-devops/docs/page-list.md)
- [api-list.md](/Users/guoqingao/workspace/golang/src/gitlab/gl-devops/docs/api-list.md)
- [project-bootstrap-plan.md](/Users/guoqingao/workspace/golang/src/gitlab/gl-devops/docs/project-bootstrap-plan.md)
