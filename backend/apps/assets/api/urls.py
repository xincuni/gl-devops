from django.urls import path

from apps.assets.api.views import (
    CloudInstanceDetailView,
    CloudInstanceJumpServerSyncView,
    CloudInstanceListView,
    CloudInstanceSyncView,
)

urlpatterns = [
    path("instances", CloudInstanceListView.as_view(), name="instance_list"),
    path("instances/<int:pk>", CloudInstanceDetailView.as_view(), name="instance_detail"),
    path("instances/<int:pk>/sync-to-jumpserver", CloudInstanceJumpServerSyncView.as_view(), name="instance_sync_jumpserver"),
    path("instances/sync", CloudInstanceSyncView.as_view(), name="instance_sync"),
]
