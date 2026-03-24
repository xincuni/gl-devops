from django.urls import path

from apps.accounts.api.views import (
    CloudAccountDetailView,
    CloudAccountListCreateView,
    CloudAccountStatusView,
    CloudAccountSyncView,
    CloudAccountTestConnectionView,
)

urlpatterns = [
    path("", CloudAccountListCreateView.as_view(), name="account_list_create"),
    path("<int:pk>", CloudAccountDetailView.as_view(), name="account_detail"),
    path("<int:pk>/status", CloudAccountStatusView.as_view(), name="account_status"),
    path("<int:pk>/test-connection", CloudAccountTestConnectionView.as_view(), name="account_test_connection"),
    path("<int:pk>/sync", CloudAccountSyncView.as_view(), name="account_sync"),
]
