from django.urls import path

from apps.domain.api.views import (
    DNSRecordBatchStatusView,
    DNSRecordBatchTTLView,
    DNSRecordDetailView,
    DNSRecordListView,
    DNSZoneDetailView,
    DNSZoneListView,
    DNSZoneSyncView,
)

urlpatterns = [
    path("zones", DNSZoneListView.as_view(), name="zone_list"),
    path("zones/<int:pk>", DNSZoneDetailView.as_view(), name="zone_detail"),
    path("zones/<int:pk>/sync", DNSZoneSyncView.as_view(), name="zone_sync"),
    path("records", DNSRecordListView.as_view(), name="record_list"),
    path("records/batch-enable", DNSRecordBatchStatusView.as_view(), {"target_status": "active"}, name="record_batch_enable"),
    path("records/batch-disable", DNSRecordBatchStatusView.as_view(), {"target_status": "disabled"}, name="record_batch_disable"),
    path("records/batch-update-ttl", DNSRecordBatchTTLView.as_view(), name="record_batch_ttl"),
    path("records/<int:pk>", DNSRecordDetailView.as_view(), name="record_detail"),
]
