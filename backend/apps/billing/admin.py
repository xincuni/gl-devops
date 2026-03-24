from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.billing.models import BillingLineItem, BillingTagRule


@admin.register(BillingTagRule)
class BillingTagRuleAdmin(ModelAdmin):
    list_display = ("name", "provider", "source_key", "target_dimension", "default_value", "is_active")
    list_filter = ("provider", "target_dimension", "is_active")
    search_fields = ("name", "source_key", "default_value")


@admin.register(BillingLineItem)
class BillingLineItemAdmin(ModelAdmin):
    list_display = (
        "billing_month",
        "provider",
        "account",
        "product",
        "resource_id",
        "discounted_cost",
        "normalized_env",
        "normalized_product",
    )
    list_filter = ("billing_month", "provider", "normalized_env", "normalized_product")
    search_fields = ("resource_id", "resource_name", "product")
