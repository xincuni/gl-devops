# 运维平台功能与技术设计

## 1. 目标

构建一个统一运维平台，解决下面几个问题：

1. 多云资源分散，缺乏统一资产视图
2. 域名解析记录分散在阿里云和 Cloudflare，无法统一治理
3. 云服务器与 JumpServer 资产不同步，维护成本高
4. 云账单数据分散，无法按业务标签分析成本

平台第一阶段以“同步、展示、批量处理、成本分析”为主，不优先做复杂自动化编排。

## 2. 核心功能

### 2.1 Portal 首页

首页建议展示：

- 云账号总数
- 域名总数、DNS 记录总数、近 24 小时变更数
- ECS/EC2 主机总数、未同步到 JumpServer 数量、同步失败数量
- 本月总费用、阿里云费用、AWS 费用
- 按标签统计的 Top N 成本项
- 最近同步任务、失败任务、告警信息

建议首页由若干卡片和趋势图组成，重点突出“异常”和“待处理”。

### 2.2 域名管理

功能范围：

- 接入阿里云 DNS 和 Cloudflare
- 同步 Zone / Domain 列表
- 同步解析记录
- 展示记录详情：主机记录、类型、线路、TTL、值、状态、更新时间、来源平台
- 对记录做治理动作：
  - 启用 / 暂停
  - 批量修改 TTL
  - 批量导出
  - 批量筛选异常记录
  - 按平台回写修改

建议设计原则：

- 本地保存“云上原始记录”和“平台规范化记录”
- 同步时保留 provider 原始字段，避免不同云字段差异造成信息丢失
- 对修改操作必须记录审计日志

可选高级功能：

- DNS 记录变更对比
- 过期证书或高风险记录识别
- CNAME/A 记录健康检查

### 2.3 服务器管理

功能范围：

- 接入阿里云 ECS 和 AWS EC2
- 定时同步实例、标签、网络信息、运行状态
- 统一展示主机资产：
  - 实例 ID
  - 主机名
  - 私网 IP / 公网 IP
  - VPC / 子网
  - 账号
  - 区域
  - 标签
  - OS 类型
  - 云厂商
  - 生命周期状态
- 根据规则将服务器同步到 JumpServer

JumpServer 同步建议支持：

- 首次推送资产
- 已存在资产匹配与更新
- 下线主机的禁用或移除策略
- 同步日志与失败重试

推荐同步逻辑：

1. 云平台同步到本地资产表
2. 本地做标准化与标签映射
3. 依据同步规则生成 JumpServer 目标资产
4. 调用 JumpServer API 创建或更新资产
5. 记录同步结果和差异

### 2.4 账单与费用分析

功能范围：

- 拉取阿里云账单明细
- 拉取 AWS Cost and Usage 数据
- 统一账单格式
- 基于标签做费用归集
- 展示月度、日度、账号、云厂商、产品线、业务标签维度分析

重点难点：

- AWS 和阿里云账单字段不一致
- 标签命名不统一，可能存在空值或多套标准
- 有些费用是实例级标签，有些费用是资源池级或产品级，不一定能完全回溯到单一资源

建议处理方式：

- 建立统一费用明细表 `billing_line_items`
- 建立标签映射规则表 `billing_tag_rules`
- 对每条账单保留原始标签 JSON 和规范化标签
- 分析时区分：
  - 原始标签视图
  - 标准标签视图

建议支持的分析维度：

- 云厂商
- 账号
- 区域
- 产品
- 资源 ID
- 环境标签，例如 `env`
- 业务标签，例如 `product`

## 3. 推荐系统架构

如果你要快速落地，我建议先走单体后端 + 前后端分离，不要一开始拆微服务。

### 3.1 后端

推荐：

- `Python` 作为后端主语言
- `Django + Django REST Framework` 作为后端框架
- `Django Admin + Unfold` 作为内部配置和运营后台
- `MySQL` 存业务数据
- `Redis` 存缓存和 Celery Broker/Backend
- `Celery + Celery Beat` 做异步和定时同步任务

原因：

- 你的场景是多平台 API 同步、任务调度、后台数据管理，Django 的交付效率更高
- DRF 适合输出标准 API 给前端
- `Django Admin + Unfold` 很适合云账号、任务记录、审计日志、CMDB 基础数据管理
- 单体架构对首版交付更稳，后面再按 provider 或领域拆分即可

### 3.2 前端

推荐：

- `Vue3 + Tailwind CSS`

页面优先级：

1. 登录
2. Portal
3. 云账号管理
4. 域名/解析记录列表
5. 服务器资产列表
6. JumpServer 同步任务列表
7. 账单分析页面

说明：

- `Django REST Framework` 作为前后端对接层
- 主要业务流程放在独立的 `Vue` 前端
- `Django Admin + Unfold` 主要给内部管理和运营使用
- `Tailwind CSS` 用于快速构建统一风格的管理界面

### 3.3 同步层

建议抽象 `provider connector`：

- `aliyun/dns`
- `aliyun/ecs`
- `aliyun/billing`
- `aws/ec2`
- `aws/billing`
- `cloudflare/dns`
- `jumpserver/asset`

统一接口示例：

```python
class SyncProvider:
    def sync(self, account_id: int) -> None:
        raise NotImplementedError
```

对不同资源再细分：

```python
class DNSProvider:
    def list_zones(self, account):
        raise NotImplementedError

    def list_records(self, account, zone_id: str):
        raise NotImplementedError


class ComputeProvider:
    def list_instances(self, account, region: str):
        raise NotImplementedError


class BillingProvider:
    def pull_bill(self, account, month: str):
        raise NotImplementedError
```

### 3.4 Django 应用划分建议

建议采用 Django app 分模块组织：

- `apps/authentication`
- `apps/accounts`
- `apps/cmdb`
- `apps/domain`
- `apps/assets`
- `apps/jumpserver`
- `apps/billing`
- `apps/tasks`
- `apps/audit`
- `apps/providers`

### 3.5 API 设计建议

建议 API 分成三类：

- 面向前端业务页面的 DRF API
- 面向内部配置管理的 Django Admin
- 面向后台任务触发和回调的内部接口

DRF 建议采用：

- `APIView` 或 `GenericAPIView + Serializer`
- 规则清晰的 `/api/v1/` 路由前缀
- 基于 Token 或 Session 的统一认证方案
- 统一响应结构、错误码和分页格式

### 3.6 Django Admin 主题优化

主题方案固定使用 `Unfold`。

建议至少做下面几项优化：

- 自定义站点标题、页头、Logo、欢迎文案
- 调整导航分组，按业务域组织菜单
- 优化 changelist 筛选项、搜索项、只读字段和详情页布局
- 基于 `Unfold` 做二次定制
- 处理 Django 默认 `User/Group` 后台在 `Unfold` 下的样式适配

设计原则：

- Admin 是高效率后台，不是默认样式直接暴露
- 优先优化运维日常高频页面
- 风格上与独立前端保持基本一致

### 3.7 任务调度设计

建议区分两类任务：

- `Celery Beat` 负责定时触发
- `Celery Worker` 负责实际同步和采集

典型任务包括：

- DNS 同步任务
- ECS 同步任务
- EC2 同步任务
- JumpServer 推送任务
- 账单采集任务
- 账单补采任务

## 4. 核心数据模型

### 4.1 云账号

`cloud_accounts`

- `id`
- `name`
- `provider`，如 `aliyun/aws/cloudflare/jumpserver`
- `credential_type`
- `credential_secret_ref`
- `status`
- `last_sync_at`

### 4.2 域名与记录

`dns_zones`

- `id`
- `account_id`
- `provider`
- `zone_id`
- `zone_name`
- `status`
- `raw_payload`
- `last_synced_at`

`dns_records`

- `id`
- `zone_id`
- `provider_record_id`
- `name`
- `type`
- `value`
- `ttl`
- `priority`
- `line`
- `enabled`
- `proxied`
- `status`
- `raw_payload`
- `last_synced_at`

### 4.3 主机资产

`cloud_instances`

- `id`
- `account_id`
- `provider`
- `region`
- `instance_id`
- `instance_name`
- `hostname`
- `private_ip`
- `public_ip`
- `os_type`
- `status`
- `vpc_id`
- `subnet_id`
- `tags_json`
- `raw_payload`
- `last_synced_at`

### 4.4 JumpServer 映射

`jumpserver_assets`

- `id`
- `instance_id`
- `jumpserver_asset_id`
- `sync_status`
- `last_sync_at`
- `last_error`

### 4.5 账单

`billing_line_items`

- `id`
- `account_id`
- `provider`
- `billing_month`
- `billing_date`
- `product_code`
- `product_name`
- `region`
- `resource_id`
- `resource_name`
- `currency`
- `original_cost`
- `discounted_cost`
- `usage_amount`
- `usage_unit`
- `tags_json`
- `normalized_tags_json`
- `raw_payload`

`billing_tag_rules`

- `id`
- `provider`
- `source_key`
- `target_key`
- `default_value`
- `enabled`

## 5. 关键流程

### 5.1 DNS 同步流程

1. 读取云账号配置
2. 拉取域名列表
3. 拉取每个域名下的解析记录
4. 写入 `dns_zones` 和 `dns_records`
5. 标记缺失记录为删除候选或失活
6. 生成同步审计日志

### 5.2 服务器同步流程

1. 拉取 ECS/EC2 实例
2. 统一实例字段
3. 写入 `cloud_instances`
4. 根据标签或规则筛选需要纳管到 JumpServer 的资产
5. 调用 JumpServer API 同步
6. 保存映射关系和错误信息

### 5.3 账单分析流程

1. 按月或按日拉取账单
2. 落原始账单明细
3. 执行标签归一化规则
4. 生成聚合表或物化视图
5. 首页和分析页查询聚合结果

## 6. 权限与审计

至少要有下面三类角色：

- `admin`：平台管理、账号管理、规则管理
- `ops`：同步任务执行、资产查看、DNS 处理
- `finance`：账单查看、成本分析、报表导出

需要审计的动作：

- 新增/修改云账号
- 手动执行同步
- 修改 DNS 记录
- 推送或移除 JumpServer 资产
- 修改标签映射规则

## 7. MVP 范围建议

第一版不要做太多，建议收敛成下面范围：

- Portal 首页基础统计
- 阿里云 DNS + Cloudflare DNS 同步与展示
- 阿里云 ECS + AWS EC2 同步与展示
- JumpServer 资产推送
- 阿里云/AWS 账单按月拉取
- 基于 `env / team / project` 三个标准标签做成本分析

第一版先不做：

- 自动修复
- 自动扩缩容
- 复杂审批流
- 多租户隔离
- 高级告警编排

## 8. 推荐开发顺序

### 阶段 1：基础底座

- 用户认证
- 云账号管理
- 任务调度框架
- 审计日志

### 阶段 2：域名模块

- 阿里云/Cloudflare 连接器
- 域名与记录同步
- 记录列表与过滤

### 阶段 3：资产模块

- ECS/EC2 同步
- 统一资产模型
- JumpServer 对接

### 阶段 4：费用模块

- 阿里云/AWS 账单采集
- 标签规则引擎
- 聚合分析接口

### 阶段 5：首页与报表

- Portal 聚合接口
- 趋势图和成本分析图表
- 任务中心

## 9. 我建议你现在就确定的三个技术决策

1. 后端是否固定使用 `Go`
2. 前端是否固定使用 `React + Ant Design`
3. 账单分析是否以 `tag` 作为主维度，还是还要支持 `成本中心/部门/项目` 等业务映射规则

如果你继续让我往下做，下一步最合适的是直接在这个仓库里初始化一个 `Go 单体后端` 的目录结构，把：

- 账号管理
- provider 抽象
- 定时同步任务框架
- 域名/资产/账单三个模块骨架

先搭出来。
