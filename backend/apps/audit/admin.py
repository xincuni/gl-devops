from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ("id", "module", "action", "operator", "target_type", "target_id", "created_at")
    list_filter = ("module", "action")
    search_fields = ("target_type", "target_id")
    readonly_fields = ("created_at",)

# Register your models here.
