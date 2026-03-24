# 运维平台项目初始化方案

## 1. 目标

这份文档用于指导项目正式进入实施阶段前的初始化工作，主要解决下面问题：

1. Django 项目如何组织目录
2. DRF 路由如何规划
3. 认证方案先选什么
4. `Unfold` 如何接入 Django Admin
5. MySQL / Redis / Celery / 前端本地开发环境如何组织

## 2. 初始化结论

建议先固定下面这些选择：

- Django 使用单体项目结构
- API 前缀固定为 `/api/v1/`
- 前端和后端完全分离
- 认证方案一期优先使用 `JWT`
- Django Admin 主题固定使用 `Unfold`
- 本地开发使用 `Docker Compose` 拉起 `MySQL + Redis`

## 3. 推荐目录结构

后端建议结构：

```text
backend/
  manage.py
  pyproject.toml
  requirements/
    base.txt
    dev.txt
    prod.txt
  config/
    __init__.py
    settings/
      __init__.py
      base.py
      local.py
      prod.py
    urls.py
    wsgi.py
    asgi.py
    celery.py
  apps/
    authentication/
    accounts/
    domain/
    assets/
    cmdb/
    jumpserver/
    billing/
    tasks/
    audit/
    providers/
    core/
  common/
    exceptions/
    pagination/
    permissions/
    responses/
    utils/
  static/
  templates/
  media/
```

前端建议结构：

```text
frontend/
  package.json
  src/
    api/
    assets/
    components/
    composables/
    layouts/
    pages/
    router/
    stores/
    styles/
    utils/
  public/
```

基础环境建议结构：

```text
deploy/
  docker/
  compose/
    local.yml
  env/
    backend.env.example
    frontend.env.example
```

## 4. Django 后端初始化建议

### 4.1 配置分层

建议按环境拆分 settings：

- `base.py`
- `local.py`
- `prod.py`

至少拆出这些配置项：

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL` 或 MySQL 连接参数
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `JWT` 相关配置
- `CORS` 白名单

### 4.2 核心依赖

后端建议依赖：

- `Django`
- `djangorestframework`
- `djangorestframework-simplejwt`
- `django-cors-headers`
- `django-filter`
- `mysqlclient` 或 `pymysql`
- `celery`
- `redis`
- `django-environ`
- `Unfold`

可选依赖：

- `drf-spectacular`
- `django-extensions`
- `flower`

### 4.3 Django apps 初始化顺序

建议先初始化这些 app：

1. `apps.core`
2. `apps.authentication`
3. `apps.accounts`
4. `apps.tasks`
5. `apps.audit`

第二批再初始化：

1. `apps.domain`
2. `apps.assets`
3. `apps.cmdb`
4. `apps.jumpserver`
5. `apps.billing`
6. `apps.providers`

## 5. DRF 路由方案

推荐采用统一版本前缀：

```text
/api/v1/
```

主路由建议：

```text
/api/v1/auth/
/api/v1/accounts/
/api/v1/domains/
/api/v1/assets/
/api/v1/cmdb/
/api/v1/jumpserver/
/api/v1/billing/
/api/v1/tasks/
/api/v1/audit/
/api/v1/portal/
```

推荐拆分方式：

- 每个 app 自己维护 `api/urls.py`
- `config/urls.py` 只做总路由聚合

建议统一的 API 规范：

- 成功响应结构统一
- 错误响应结构统一
- 分页结构统一
- 列表筛选参数命名统一
- 异步触发型接口统一返回 `task_id`

## 6. 认证方案建议

### 推荐选择

一期建议优先使用 `JWT`，基于 `djangorestframework-simplejwt` 实现。

原因：

- 前后端分离更适合 `JWT`
- Vue 前端更容易管理登录态
- 后续如果开放多端接入也更方便

### 登录相关接口建议

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

### 注意点

- Access Token 设置较短过期时间
- Refresh Token 做失效和轮换策略
- 前端统一处理 401 刷新逻辑

如果你更偏向 Django 原生后台一致性，也可以选 `Session`，但对独立前端没有 `JWT` 直接。

## 7. Unfold 接入方案

### 7.1 基础接入

建议在一期就完成下面几项：

- 安装 `Unfold`
- 配置站点标题、页头、Logo、品牌名称
- 配置菜单分组
- 为核心模型使用统一 Admin 基类

### 7.2 Admin 基类建议

建议封装项目统一基类，例如：

- `BaseAdmin`
- `TimestampedAdmin`
- `AuditReadonlyAdmin`

这样后续模型页不用反复写相同配置。

### 7.3 用户和权限模型适配

按照 `Unfold` 官方文档，Django 默认的 `User/Group` 后台需要重新注册并使用 `unfold.admin.ModelAdmin` 风格，否则样式不会统一。

建议初始化阶段就处理：

- `User` admin
- `Group` admin
- 用户创建表单
- 用户修改表单
- 密码修改表单

### 7.4 一期优先优化的 Admin 页面

- 云账号
- 任务记录
- 审计日志
- 标签规则
- JumpServer 同步规则

## 8. Celery 初始化方案

### 8.1 进程划分

建议本地至少跑这三个进程：

- Django API Server
- Celery Worker
- Celery Beat

可选：

- Flower

### 8.2 任务命名建议

任务建议按领域命名：

- `domain.sync_zones`
- `domain.sync_records`
- `assets.sync_ecs_instances`
- `assets.sync_ec2_instances`
- `jumpserver.sync_assets`
- `billing.collect_aliyun_bill`
- `billing.collect_aws_bill`

### 8.3 任务设计原则

- 任务尽量幂等
- 长任务支持重试
- 每次执行记录任务日志
- 大批量同步按账号或区域拆分子任务

## 9. 本地开发环境方案

建议本地依赖：

- `MySQL`
- `Redis`

推荐使用 `Docker Compose`。

推荐本地启动组合：

```text
mysql
redis
backend
worker
beat
frontend
```

建议约定端口：

- Django API：`8000`
- Vue Dev Server：`5173`
- MySQL：`3306`
- Redis：`6379`
- Flower：`5555`

## 10. 初始化阶段的实施顺序

建议按下面顺序执行：

1. 初始化 `backend/` 和 Django 项目
2. 初始化 `frontend/` 和 Vue 项目
3. 配置 MySQL、Redis、Celery
4. 接入 DRF、JWT、CORS
5. 接入 `Unfold`
6. 建立基础 app 和公共模块
7. 建立登录、账号、任务、审计的基础骨架

## 11. 初始化阶段验收标准

满足下面条件后，就可以正式进入业务开发：

- Django 项目可启动
- Vue 项目可启动
- `JWT` 登录接口可用
- DRF 基础路由可用
- `Unfold` 后台可访问
- `User/Group` 后台样式已适配
- MySQL、Redis、Celery Worker、Celery Beat 可运行
- 云账号模块基础表和基础 API 已建立

## 12. 后续直接可做的第一批任务

初始化完成后，建议立刻进入下面任务：

1. 云账号 CRUD
2. 云账号连通性测试
3. 任务记录模型
4. 审计日志模型
5. DNS provider 骨架
