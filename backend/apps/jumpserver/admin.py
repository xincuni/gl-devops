from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.jumpserver.models import JumpServerSyncLog, JumpServerSyncRule


@admin.register(JumpServerSyncRule)
class JumpServerSyncRuleAdmin(ModelAdmin):
    list_display = ("name", "provider", "region", "env", "node_path", "status", "priority")
    list_filter = ("status", "provider", "region", "env")
    search_fields = ("name", "node_path")


@admin.register(JumpServerSyncLog)
class JumpServerSyncLogAdmin(ModelAdmin):
    list_display = ("instance", "rule", "status", "jumpserver_asset_id", "synced_at")
    list_filter = ("status",)
    search_fields = ("instance__instance_name", "jumpserver_asset_id", "message")
