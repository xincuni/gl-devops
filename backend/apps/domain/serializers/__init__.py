from rest_framework import serializers

from apps.domain.models import DNSRecord, DNSZone


class DNSZoneSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source="account.name", read_only=True)
    record_count = serializers.IntegerField(source="records.count", read_only=True)

    class Meta:
        model = DNSZone
        fields = "__all__"


class DNSRecordSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source="zone.zone_name", read_only=True)
    provider = serializers.CharField(source="zone.provider", read_only=True)

    class Meta:
        model = DNSRecord
        fields = "__all__"
