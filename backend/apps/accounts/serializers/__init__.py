from rest_framework import serializers

from apps.accounts.models import CloudAccount


class CloudAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudAccount
        fields = "__all__"
        read_only_fields = ("id", "last_sync_at", "created_at", "updated_at")
