from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from apps.assets.models import CloudInstance
from apps.jumpserver.models import JumpServerSyncLog, JumpServerSyncRule
from apps.jumpserver.serializers import JumpServerSyncLogSerializer, JumpServerSyncRuleSerializer
from apps.jumpserver.services import sync_instances_to_jumpserver
from common.responses import success_response


class JumpServerSyncRuleListCreateView(generics.ListCreateAPIView):
    queryset = JumpServerSyncRule.objects.select_related("account").all()
    serializer_class = JumpServerSyncRuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "provider", "region", "env", "account"]
    search_fields = ["name", "node_path"]


class JumpServerSyncRuleDetailView(generics.RetrieveUpdateAPIView):
    queryset = JumpServerSyncRule.objects.select_related("account").all()
    serializer_class = JumpServerSyncRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class JumpServerSyncLogListView(generics.ListAPIView):
    queryset = JumpServerSyncLog.objects.select_related("instance", "rule").all()
    serializer_class = JumpServerSyncLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "rule", "instance"]
    search_fields = ["instance__instance_name", "message", "jumpserver_asset_id"]


class JumpServerSyncLogDetailView(generics.RetrieveAPIView):
    queryset = JumpServerSyncLog.objects.select_related("instance", "rule").all()
    serializer_class = JumpServerSyncLogSerializer
    permission_classes = [permissions.IsAuthenticated]


class JumpServerSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        instance_ids = request.data.get("instance_ids", [])
        instances = CloudInstance.objects.filter(id__in=instance_ids) if instance_ids else CloudInstance.objects.all()[:10]
        task = sync_instances_to_jumpserver(instances=list(instances), operator=request.user)
        return success_response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
