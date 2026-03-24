from django.db import models

from apps.accounts.models import CloudAccount


class CloudInstance(models.Model):
    class JumpServerSyncStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SYNCED = "synced", "Synced"
        FAILED = "failed", "Failed"

    class Status(models.TextChoices):
        RUNNING = "running", "Running"
        STOPPED = "stopped", "Stopped"
        TERMINATED = "terminated", "Terminated"

    account = models.ForeignKey(CloudAccount, on_delete=models.CASCADE, related_name="instances")
    provider = models.CharField(max_length=32)
    region = models.CharField(max_length=64)
    instance_id = models.CharField(max_length=128)
    instance_name = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255, blank=True)
    private_ip = models.CharField(max_length=64, blank=True)
    public_ip = models.CharField(max_length=64, blank=True)
    os_type = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.RUNNING)
    vpc_id = models.CharField(max_length=128, blank=True)
    subnet_id = models.CharField(max_length=128, blank=True)
    tags_json = models.JSONField(default=dict, blank=True)
    sync_status = models.CharField(max_length=32, default="pending")
    jumpserver_sync_status = models.CharField(
        max_length=16,
        choices=JumpServerSyncStatus.choices,
        default=JumpServerSyncStatus.PENDING,
    )
    jumpserver_asset_id = models.CharField(max_length=128, blank=True)
    last_jumpserver_sync_at = models.DateTimeField(null=True, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["provider", "region", "instance_name"]
        unique_together = ("account", "instance_id")

    def __str__(self):
        return self.instance_name or self.instance_id
