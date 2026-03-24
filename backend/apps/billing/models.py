from django.db import models

from apps.accounts.models import CloudAccount


class BillingTagRule(models.Model):
    class Dimension(models.TextChoices):
        ENV = "env", "Env"
        PRODUCT = "product", "Product"

    name = models.CharField(max_length=128, unique=True)
    provider = models.CharField(max_length=32, blank=True)
    source_key = models.CharField(max_length=128)
    target_dimension = models.CharField(max_length=16, choices=Dimension.choices)
    default_value = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["target_dimension", "name"]

    def __str__(self):
        return self.name


class BillingLineItem(models.Model):
    billing_month = models.CharField(max_length=7)
    billing_date = models.DateField()
    provider = models.CharField(max_length=32)
    account = models.ForeignKey(CloudAccount, on_delete=models.CASCADE, related_name="billing_line_items")
    product = models.CharField(max_length=128)
    resource_id = models.CharField(max_length=128)
    resource_name = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=16, default="CNY")
    original_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discounted_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usage_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usage_unit = models.CharField(max_length=32, default="hour")
    tag_data = models.JSONField(default=dict, blank=True)
    normalized_env = models.CharField(max_length=64, blank=True)
    normalized_product = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-billing_date", "provider", "product"]

    def __str__(self):
        return f"{self.provider}:{self.product}:{self.resource_id}"
