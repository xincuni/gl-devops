from django.urls import path

from apps.audit.api.views import AuditLogDetailView, AuditLogListView

urlpatterns = [
    path("logs", AuditLogListView.as_view(), name="audit_log_list"),
    path("logs/<int:pk>", AuditLogDetailView.as_view(), name="audit_log_detail"),
]
