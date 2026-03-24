# 运维平台系统模块清单

## 1. 模块分层

一期建议按下面四层组织系统：

1. 接入层：认证、权限、API、Admin
2. 业务层：账号、域名、主机、CMDB、JumpServer、账单、费用分析
3. 调度层：Celery 任务、定时任务、重试、补采
4. 支撑层：审计日志、通知、缓存、文件导出、系统配置

## 2. Django 后端模块

### 2.1 `apps/authentication`

职责：

- 登录认证
- Token / Session 管理
- 当前用户信息
- 权限校验

主要能力：

- 登录接口
- 登出接口
- 用户信息接口
- 权限点输出

### 2.2 `apps/accounts`

职责：

- 管理云账号和外部系统连接

主要能力：

- 阿里云账号管理
- AWS 账号管理
- Cloudflare 账号管理
- JumpServer 连接管理
- 连通性测试
- 首次同步触发

核心对象：

- `cloud_accounts`

### 2.3 `apps/domain`

职责：

- 域名和 DNS 记录管理

主要能力：

- 域名同步
- 解析记录同步
- 记录列表查询
- 记录详情查看
- TTL 批量修改
- 启用/停用记录
- 导出记录

核心对象：

- `dns_zones`
- `dns_records`

### 2.4 `apps/assets`

职责：

- 云服务器资产同步与管理

主要能力：

- ECS 同步
- EC2 同步
- 主机列表
- 主机详情
- 标签管理
- 状态展示

核心对象：

- `cloud_instances`

### 2.5 `apps/cmdb`

职责：

- 承载统一资产模型

主要能力：

- 资产主表管理
- 资产标准字段管理
- 资产来源标记
- 资产关联关系
- CMDB 查询视图

一期纳入对象：

- 云账号
- 云主机
- 域名
- DNS 记录
- JumpServer 资产映射

### 2.6 `apps/jumpserver`

职责：

- 管理 JumpServer 对接与资产纳管

主要能力：

- 同步规则管理
- 主机推送
- 资产更新
- 下线处理
- 同步日志
- 失败重试

核心对象：

- `jumpserver_assets`
- `jumpserver_sync_logs`

### 2.7 `apps/billing`

职责：

- 账单采集与成本分析

主要能力：

- 阿里云账单采集
- AWS 账单采集
- 补采任务
- 标签归一化
- 聚合分析
- 报表导出

核心对象：

- `billing_line_items`
- `billing_tag_rules`
- `billing_daily_summaries`

### 2.8 `apps/tasks`

职责：

- 管理异步任务和定时任务

主要能力：

- Celery 任务注册
- Beat 调度配置
- 任务执行记录
- 重试和补偿
- 任务状态查询

主要任务：

- DNS 同步
- ECS/EC2 同步
- JumpServer 推送
- 账单采集
- 账单补采

### 2.9 `apps/audit`

职责：

- 记录关键操作审计日志

主要能力：

- 云账号变更审计
- DNS 修改审计
- JumpServer 纳管审计
- 任务执行审计
- 规则变更审计

### 2.10 `apps/providers`

职责：

- 统一管理各类 provider connector

子模块建议：

- `providers.aliyun_dns`
- `providers.aliyun_ecs`
- `providers.aliyun_billing`
- `providers.aws_ec2`
- `providers.aws_billing`
- `providers.cloudflare_dns`
- `providers.jumpserver`

职责边界：

- 负责外部 API 对接和数据标准化
- 不负责业务页面逻辑
- 不直接承担页面聚合查询

## 3. 前端模块

### 3.1 `portal`

- 首页卡片、趋势图、异常提示、最近任务

### 3.2 `accounts`

- 云账号列表、创建、编辑、连通性测试、手动同步

### 3.3 `domains`

- 域名列表、记录列表、记录详情、批量操作

### 3.4 `assets`

- 主机列表、详情、筛选、JumpServer 状态展示

### 3.5 `cmdb`

- 统一资产列表、资产详情、资产关系视图

### 3.6 `billing`

- 费用总览、趋势、按 `env/product` 分析、Top 成本排行

### 3.7 `tasks`

- 任务列表、任务详情、失败重试

### 3.8 `audit`

- 审计日志列表、筛选、详情

## 4. Admin 模块

`Django Admin + Unfold` 主要承担内部配置和运营后台：

- 云账号配置
- 标签规则配置
- 同步规则配置
- 任务记录查看
- 审计日志查看
- CMDB 基础数据维护

主题优化要求：

- 基于 `Unfold` 实现统一后台主题
- 自定义品牌
- 菜单分组
- 高亮常用模块
- 优化筛选和搜索

## 5. 模块依赖关系

建议依赖顺序：

1. `authentication`
2. `accounts`
3. `providers`
4. `tasks`
5. `domain / assets / billing`
6. `jumpserver`
7. `cmdb`
8. `portal / audit`
