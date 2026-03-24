from rest_framework import serializers

from apps.billing.models import BillingLineItem, BillingTagRule


class BillingTagRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingTagRule
        fields = "__all__"


class BillingLineItemSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source="account.name", read_only=True)

    class Meta:
        model = BillingLineItem
        fields = "__all__"
