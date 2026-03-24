from rest_framework import serializers

from apps.jumpserver.models import JumpServerSyncLog, JumpServerSyncRule


class JumpServerSyncRuleSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source="account.name", read_only=True)

    class Meta:
        model = JumpServerSyncRule
        fields = "__all__"


class JumpServerSyncLogSerializer(serializers.ModelSerializer):
    instance_name = serializers.CharField(source="instance.instance_name", read_only=True)
    rule_name = serializers.CharField(source="rule.name", read_only=True)

    class Meta:
        model = JumpServerSyncLog
        fields = "__all__"
