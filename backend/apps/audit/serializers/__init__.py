from rest_framework import serializers

from apps.audit.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    operator_username = serializers.CharField(source="operator.username", read_only=True)

    class Meta:
        model = AuditLog
        fields = "__all__"
