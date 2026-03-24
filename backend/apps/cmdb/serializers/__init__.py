from rest_framework import serializers

from apps.cmdb.models import CMDBAsset


class CMDBAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBAsset
        fields = "__all__"
