from rest_framework import generics, permissions

from apps.audit.models import AuditLog
from apps.audit.serializers import AuditLogSerializer


class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.select_related("operator").all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["module", "action", "operator"]
    search_fields = ["target_type", "target_id"]


class AuditLogDetailView(generics.RetrieveAPIView):
    queryset = AuditLog.objects.select_related("operator").all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
