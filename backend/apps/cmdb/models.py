from django.db import models


class CMDBAsset(models.Model):
    class AssetType(models.TextChoices):
        CLOUD_ACCOUNT = "cloud_account", "Cloud Account"
        CLOUD_INSTANCE = "cloud_instance", "Cloud Instance"
        DNS_ZONE = "dns_zone", "DNS Zone"
        DNS_RECORD = "dns_record", "DNS Record"

    asset_type = models.CharField(max_length=32, choices=AssetType.choices)
    source = models.CharField(max_length=32)
    source_ref = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=32, default="active")
    labels = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["asset_type", "name"]
        unique_together = ("asset_type", "source", "source_ref")

    def __str__(self):
        return self.name
