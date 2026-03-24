from rest_framework import serializers

from apps.assets.models import CloudInstance


class CloudInstanceSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source="account.name", read_only=True)

    class Meta:
        model = CloudInstance
        fields = "__all__"
