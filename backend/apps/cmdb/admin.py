from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.cmdb.models import CMDBAsset


@admin.register(CMDBAsset)
class CMDBAssetAdmin(ModelAdmin):
    list_display = ("id", "name", "asset_type", "source", "status", "last_synced_at")
    list_filter = ("asset_type", "source", "status")
    search_fields = ("name", "source_ref")
