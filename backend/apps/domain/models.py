from django.db import models

from apps.accounts.models import CloudAccount


class DNSZone(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DISABLED = "disabled", "Disabled"

    account = models.ForeignKey(CloudAccount, on_delete=models.CASCADE, related_name="dns_zones")
    provider = models.CharField(max_length=32)
    zone_id = models.CharField(max_length=128)
    zone_name = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    raw_payload = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["zone_name"]
        unique_together = ("account", "zone_id")

    def __str__(self):
        return self.zone_name


class DNSRecord(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DISABLED = "disabled", "Disabled"

    zone = models.ForeignKey(DNSZone, on_delete=models.CASCADE, related_name="records")
    provider_record_id = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=32)
    value = models.CharField(max_length=512)
    ttl = models.PositiveIntegerField(default=600)
    line = models.CharField(max_length=64, blank=True)
    priority = models.PositiveIntegerField(default=0)
    proxied = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    raw_payload = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["zone__zone_name", "name", "type"]
        unique_together = ("zone", "provider_record_id")

    def __str__(self):
        return f"{self.name} {self.type}"
