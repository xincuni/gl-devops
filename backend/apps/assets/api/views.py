from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from apps.accounts.models import CloudAccount
from apps.assets.models import CloudInstance
from apps.assets.serializers import CloudInstanceSerializer
from apps.assets.services import seed_instance_sync
from apps.jumpserver.services import sync_instances_to_jumpserver
from common.responses import success_response


class CloudInstanceListView(generics.ListAPIView):
    queryset = CloudInstance.objects.select_related("account").all()
    serializer_class = CloudInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["provider", "account", "region", "status", "sync_status", "jumpserver_sync_status"]
    search_fields = ["instance_name", "instance_id", "private_ip", "public_ip"]


class CloudInstanceDetailView(generics.RetrieveAPIView):
    queryset = CloudInstance.objects.select_related("account").all()
    serializer_class = CloudInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]


class CloudInstanceSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        account_ids = request.data.get("account_ids", [])
        accounts = CloudAccount.objects.filter(id__in=account_ids) if account_ids else CloudAccount.objects.filter(provider__in=["aliyun", "aws"])
        task_ids = [seed_instance_sync(account=account, operator=request.user).id for account in accounts]
        return success_response({"task_ids": task_ids}, status=status.HTTP_202_ACCEPTED)


class CloudInstanceJumpServerSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        instance = generics.get_object_or_404(CloudInstance, pk=pk)
        task = sync_instances_to_jumpserver(instances=[instance], operator=request.user)
        return success_response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
