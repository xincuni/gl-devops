# 运维平台 DRF API 清单

## 1. API 设计约定

- 路由前缀使用 `/api/v1`
- 返回 JSON
- 列表接口统一支持分页
- 列表接口统一支持关键筛选条件
- 所有写操作保留审计日志
- 长耗时操作尽量走异步任务，接口只负责触发和返回任务 ID

## 2. 认证与用户

### 登录认证

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

### 权限信息

- `GET /api/v1/auth/permissions`

## 3. 云账号

### 账号管理

- `GET /api/v1/accounts`
- `POST /api/v1/accounts`
- `GET /api/v1/accounts/{id}`
- `PUT /api/v1/accounts/{id}`
- `PATCH /api/v1/accounts/{id}/status`
- `POST /api/v1/accounts/{id}/test-connection`
- `POST /api/v1/accounts/{id}/sync`

关键筛选：

- `provider`
- `status`
- `keyword`

## 4. 域名与 DNS

### 域名

- `GET /api/v1/domains/zones`
- `GET /api/v1/domains/zones/{id}`
- `POST /api/v1/domains/zones/{id}/sync`

关键筛选：

- `provider`
- `account_id`
- `zone_name`

### DNS 记录

- `GET /api/v1/domains/records`
- `GET /api/v1/domains/records/{id}`
- `POST /api/v1/domains/records/batch-enable`
- `POST /api/v1/domains/records/batch-disable`
- `POST /api/v1/domains/records/batch-update-ttl`
- `GET /api/v1/domains/records/export`

关键筛选：

- `zone_id`
- `provider`
- `type`
- `name`
- `status`

### DNS 审计

- `GET /api/v1/domains/records/{id}/audits`

## 5. 主机资产

### 云主机

- `GET /api/v1/assets/instances`
- `GET /api/v1/assets/instances/{id}`
- `POST /api/v1/assets/instances/sync`
- `POST /api/v1/assets/instances/{id}/sync-to-jumpserver`

关键筛选：

- `provider`
- `account_id`
- `region`
- `status`
- `tag`
- `jumpserver_sync_status`

## 6. CMDB

### 统一资产

- `GET /api/v1/cmdb/assets`
- `GET /api/v1/cmdb/assets/{id}`

关键筛选：

- `asset_type`
- `source`
- `status`
- `keyword`

## 7. JumpServer

### 同步规则

- `GET /api/v1/jumpserver/rules`
- `POST /api/v1/jumpserver/rules`
- `GET /api/v1/jumpserver/rules/{id}`
- `PUT /api/v1/jumpserver/rules/{id}`
- `PATCH /api/v1/jumpserver/rules/{id}/status`

### 同步任务与记录

- `POST /api/v1/jumpserver/sync`
- `GET /api/v1/jumpserver/sync-logs`
- `GET /api/v1/jumpserver/sync-logs/{id}`
- `POST /api/v1/jumpserver/sync-logs/{id}/retry`

关键筛选：

- `rule_id`
- `status`
- `account_id`

## 8. 账单与成本

### 账单采集

- `POST /api/v1/billing/collect`
- `POST /api/v1/billing/recollect`
- `GET /api/v1/billing/collect-logs`

### 账单明细

- `GET /api/v1/billing/line-items`
- `GET /api/v1/billing/line-items/{id}`

关键筛选：

- `provider`
- `account_id`
- `billing_month`
- `product`
- `resource_id`

### 费用分析

- `GET /api/v1/billing/overview`
- `GET /api/v1/billing/analysis/by-env`
- `GET /api/v1/billing/analysis/by-product`
- `GET /api/v1/billing/analysis/by-account`
- `GET /api/v1/billing/analysis/by-resource`
- `GET /api/v1/billing/analysis/trend`

关键筛选：

- `start_date`
- `end_date`
- `provider`
- `account_id`
- `env`
- `product`

## 9. 任务中心

### 异步任务

- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{id}`
- `POST /api/v1/tasks/{id}/retry`

关键筛选：

- `task_type`
- `status`
- `created_by`
- `date_from`
- `date_to`

## 10. 审计日志

### 审计查询

- `GET /api/v1/audit/logs`
- `GET /api/v1/audit/logs/{id}`

关键筛选：

- `module`
- `action`
- `operator`
- `date_from`
- `date_to`

## 11. Portal 聚合接口

### 首页聚合

- `GET /api/v1/portal/summary`
- `GET /api/v1/portal/recent-tasks`
- `GET /api/v1/portal/alerts`

## 12. 一期优先实现 API

建议先做下面这些：

1. `auth`
2. `accounts`
3. `domains/records`
4. `assets/instances`
5. `billing/overview`
6. `tasks`
7. `portal/summary`
