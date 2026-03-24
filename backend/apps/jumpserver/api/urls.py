from django.urls import path

from apps.jumpserver.api.views import (
    JumpServerSyncLogDetailView,
    JumpServerSyncLogListView,
    JumpServerSyncRuleDetailView,
    JumpServerSyncRuleListCreateView,
    JumpServerSyncView,
)

urlpatterns = [
    path("rules", JumpServerSyncRuleListCreateView.as_view(), name="jumpserver_rule_list"),
    path("rules/<int:pk>", JumpServerSyncRuleDetailView.as_view(), name="jumpserver_rule_detail"),
    path("sync", JumpServerSyncView.as_view(), name="jumpserver_sync"),
    path("sync-logs", JumpServerSyncLogListView.as_view(), name="jumpserver_sync_log_list"),
    path("sync-logs/<int:pk>", JumpServerSyncLogDetailView.as_view(), name="jumpserver_sync_log_detail"),
]
