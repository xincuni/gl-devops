from django.db import models


class CloudAccount(models.Model):
    class Provider(models.TextChoices):
        ALIYUN = "aliyun", "Aliyun"
        AWS = "aws", "AWS"
        CLOUDFLARE = "cloudflare", "Cloudflare"
        JUMPSERVER = "jumpserver", "JumpServer"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DISABLED = "disabled", "Disabled"

    name = models.CharField(max_length=128, unique=True)
    provider = models.CharField(max_length=32, choices=Provider.choices)
    access_key = models.CharField(max_length=255, blank=True)
    secret_key = models.CharField(max_length=255, blank=True)
    extra_config = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    last_sync_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.provider})"

# Create your models here.
