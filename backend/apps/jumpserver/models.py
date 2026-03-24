from django.db import models

from apps.accounts.models import CloudAccount


class JumpServerSyncRule(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DISABLED = "disabled", "Disabled"

    name = models.CharField(max_length=128, unique=True)
    account = models.ForeignKey(
        CloudAccount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="jumpserver_rules",
    )
    provider = models.CharField(max_length=32, blank=True)
    region = models.CharField(max_length=64, blank=True)
    env = models.CharField(max_length=64, blank=True)
    node_path = models.CharField(max_length=255, blank=True)
    platform = models.CharField(max_length=64, default="linux")
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    priority = models.PositiveIntegerField(default=100)
    extra_config = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "name"]

    def __str__(self):
        return self.name


class JumpServerSyncLog(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    rule = models.ForeignKey(
        JumpServerSyncRule,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sync_logs",
    )
    instance = models.ForeignKey(
        "assets.CloudInstance",
        on_delete=models.CASCADE,
        related_name="jumpserver_sync_logs",
    )
    jumpserver_asset_id = models.CharField(max_length=128, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.SUCCESS)
    message = models.CharField(max_length=255, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-synced_at"]

    def __str__(self):
        return f"{self.instance.instance_name} [{self.status}]"
