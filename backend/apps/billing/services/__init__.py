from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from apps.accounts.models import CloudAccount
from apps.audit.services import write_audit_log
from apps.billing.models import BillingLineItem, BillingTagRule
from apps.tasks.models import TaskExecution


def ensure_default_tag_rules():
    defaults = [
        {"name": "Aliyun Env Tag", "provider": "aliyun", "source_key": "env", "target_dimension": BillingTagRule.Dimension.ENV, "default_value": "unknown"},
        {"name": "AWS Env Tag", "provider": "aws", "source_key": "Environment", "target_dimension": BillingTagRule.Dimension.ENV, "default_value": "unknown"},
        {"name": "Aliyun Product Tag", "provider": "aliyun", "source_key": "product", "target_dimension": BillingTagRule.Dimension.PRODUCT, "default_value": "shared"},
        {"name": "AWS Product Tag", "provider": "aws", "source_key": "Product", "target_dimension": BillingTagRule.Dimension.PRODUCT, "default_value": "shared"},
    ]
    for item in defaults:
        BillingTagRule.objects.update_or_create(name=item["name"], defaults=item)


def _resolve_dimension(provider, tags, dimension):
    rules = BillingTagRule.objects.filter(is_active=True, target_dimension=dimension).filter(provider__in=["", provider]).order_by("-provider", "id")
    for rule in rules:
        if rule.source_key in tags and tags.get(rule.source_key):
            return str(tags.get(rule.source_key))
    fallback = rules.first()
    return fallback.default_value if fallback else ""


def seed_billing_data(*, operator=None):
    ensure_default_tag_rules()
    month = timezone.localdate().strftime("%Y-%m")
    today = timezone.localdate()
    samples = {
        "aliyun": [
            {"product": "ECS", "resource_id": "i-aliyun-web-01", "resource_name": "aliyun-web-01", "cost": Decimal("320.50"), "currency": "CNY", "tags": {"env": "prod", "product": "portal"}},
            {"product": "SLB", "resource_id": "slb-aliyun-01", "resource_name": "aliyun-slb-01", "cost": Decimal("88.00"), "currency": "CNY", "tags": {"env": "prod", "product": "portal"}},
            {"product": "RDS", "resource_id": "rds-aliyun-01", "resource_name": "aliyun-rds-01", "cost": Decimal("210.30"), "currency": "CNY", "tags": {"env": "staging", "product": "ops"}},
        ],
        "aws": [
            {"product": "EC2", "resource_id": "i-aws-web-01", "resource_name": "aws-web-01", "cost": Decimal("410.80"), "currency": "USD", "tags": {"Environment": "prod", "Product": "portal"}},
            {"product": "NAT", "resource_id": "nat-aws-01", "resource_name": "aws-nat-01", "cost": Decimal("96.40"), "currency": "USD", "tags": {"Environment": "prod", "Product": "infra"}},
            {"product": "S3", "resource_id": "s3-aws-logs", "resource_name": "aws-logs", "cost": Decimal("45.60"), "currency": "USD", "tags": {"Environment": "shared", "Product": "ops"}},
        ],
    }

    created = 0
    accounts = CloudAccount.objects.filter(provider__in=[CloudAccount.Provider.ALIYUN, CloudAccount.Provider.AWS])
    for account in accounts:
        for item in samples.get(account.provider, []):
            env = _resolve_dimension(account.provider, item["tags"], BillingTagRule.Dimension.ENV)
            product = _resolve_dimension(account.provider, item["tags"], BillingTagRule.Dimension.PRODUCT)
            BillingLineItem.objects.update_or_create(
                account=account,
                billing_month=month,
                resource_id=item["resource_id"],
                defaults={
                    "billing_date": today,
                    "provider": account.provider,
                    "product": item["product"],
                    "resource_name": item["resource_name"],
                    "currency": item["currency"],
                    "original_cost": item["cost"],
                    "discounted_cost": item["cost"],
                    "usage_quantity": Decimal("720"),
                    "usage_unit": "hour",
                    "tag_data": item["tags"],
                    "normalized_env": env,
                    "normalized_product": product,
                },
            )
            created += 1

    task = TaskExecution.objects.create(
        name=f"Collect billing for {month}",
        task_type=TaskExecution.TaskType.BILLING_COLLECT,
        status=TaskExecution.Status.SUCCESS,
        message="mock billing collect completed",
        payload={"month": month},
        result={"line_items": created},
        created_by=operator,
        started_at=timezone.now(),
        finished_at=timezone.now(),
    )
    write_audit_log(
        module="billing",
        action="collect",
        operator=operator,
        target_type="billing_month",
        target_id=month,
        detail={"task_id": task.id, "line_items": created},
    )
    return task


def billing_overview():
    queryset = BillingLineItem.objects.all()
    totals_by_currency = queryset.values("currency").annotate(total=Sum("discounted_cost")).order_by("currency")
    by_provider = queryset.values("provider", "currency").annotate(total=Sum("discounted_cost")).order_by("provider", "currency")
    months = queryset.values_list("billing_month", flat=True).distinct().order_by("-billing_month")
    return {
        "line_item_count": queryset.count(),
        "months": list(months),
        "totals_by_currency": [{"currency": item["currency"], "total_cost": float(item["total"] or 0)} for item in totals_by_currency],
        "provider_breakdown": [
            {
                "provider": item["provider"],
                "currency": item["currency"],
                "total_cost": float(item["total"] or 0),
            }
            for item in by_provider
        ],
    }


def analysis_by_dimension(dimension):
    field_name = "normalized_env" if dimension == "env" else "normalized_product"
    rows = BillingLineItem.objects.values(field_name, "currency").annotate(total=Sum("discounted_cost")).order_by("currency", "-total", field_name)
    return [
        {
            dimension: item[field_name] or "unknown",
            "currency": item["currency"],
            "total_cost": float(item["total"] or 0),
        }
        for item in rows
    ]


def analysis_by_account():
    rows = BillingLineItem.objects.values("account__name", "provider", "currency").annotate(total=Sum("discounted_cost")).order_by("currency", "-total")
    return [{"account_name": item["account__name"], "provider": item["provider"], "currency": item["currency"], "total_cost": float(item["total"] or 0)} for item in rows]


def analysis_by_resource():
    rows = BillingLineItem.objects.values("resource_id", "resource_name", "product", "currency").annotate(total=Sum("discounted_cost")).order_by("currency", "-total")[:10]
    return [
        {
            "resource_id": item["resource_id"],
            "resource_name": item["resource_name"],
            "product": item["product"],
            "currency": item["currency"],
            "total_cost": float(item["total"] or 0),
        }
        for item in rows
    ]


def analysis_trend():
    bucket = defaultdict(Decimal)
    for item in BillingLineItem.objects.all():
        bucket[(str(item.billing_date), item.currency)] += item.discounted_cost
    return [{"date": date, "currency": currency, "total_cost": float(total)} for (date, currency), total in sorted(bucket.items())]
