from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from apps.cmdb.models import CMDBAsset
from apps.cmdb.serializers import CMDBAssetSerializer
from apps.cmdb.services import sync_cmdb_assets
from common.responses import success_response


class CMDBAssetListView(generics.ListAPIView):
    queryset = CMDBAsset.objects.all()
    serializer_class = CMDBAssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["asset_type", "source", "status"]
    search_fields = ["name", "source_ref"]
    ordering_fields = ["asset_type", "source", "status", "name", "last_synced_at", "created_at"]


class CMDBAssetDetailView(generics.RetrieveAPIView):
    queryset = CMDBAsset.objects.all()
    serializer_class = CMDBAssetSerializer
    permission_classes = [permissions.IsAuthenticated]


class CMDBSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sync_cmdb_assets()
        return success_response({"synced": True}, status=status.HTTP_202_ACCEPTED)
