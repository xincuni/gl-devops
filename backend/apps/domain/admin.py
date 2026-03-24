from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.domain.models import DNSRecord, DNSZone


@admin.register(DNSZone)
class DNSZoneAdmin(ModelAdmin):
    list_display = ("id", "zone_name", "provider", "account", "status", "last_synced_at")
    list_filter = ("provider", "status")
    search_fields = ("zone_name", "zone_id")


@admin.register(DNSRecord)
class DNSRecordAdmin(ModelAdmin):
    list_display = ("id", "zone", "name", "type", "value", "ttl", "status")
    list_filter = ("type", "status", "zone__provider")
    search_fields = ("name", "value", "provider_record_id")
