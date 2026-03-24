from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.accounts.models import CloudAccount


@admin.register(CloudAccount)
class CloudAccountAdmin(ModelAdmin):
    list_display = ("id", "name", "provider", "status", "last_sync_at", "updated_at")
    list_filter = ("provider", "status")
    search_fields = ("name",)

# Register your models here.
