from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.assets.models import CloudInstance


@admin.register(CloudInstance)
class CloudInstanceAdmin(ModelAdmin):
    list_display = ("id", "instance_name", "provider", "region", "private_ip", "status", "sync_status")
    list_filter = ("provider", "region", "status", "sync_status")
    search_fields = ("instance_name", "instance_id", "private_ip", "public_ip")
