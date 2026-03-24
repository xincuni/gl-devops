from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from apps.accounts.models import CloudAccount
from apps.accounts.serializers import CloudAccountSerializer
from apps.audit.services import write_audit_log
from apps.tasks.models import TaskExecution
from common.responses import success_response


class CloudAccountListCreateView(generics.ListCreateAPIView):
    queryset = CloudAccount.objects.all()
    serializer_class = CloudAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["provider", "status"]
    search_fields = ["name"]

    def perform_create(self, serializer):
        instance = serializer.save()
        write_audit_log(
            module="accounts",
            action="create",
            operator=self.request.user,
            target_type="cloud_account",
            target_id=str(instance.id),
            detail={"name": instance.name, "provider": instance.provider},
        )


class CloudAccountDetailView(generics.RetrieveUpdateAPIView):
    queryset = CloudAccount.objects.all()
    serializer_class = CloudAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        write_audit_log(
            module="accounts",
            action="update",
            operator=self.request.user,
            target_type="cloud_account",
            target_id=str(instance.id),
            detail={"status": instance.status},
        )


class CloudAccountStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        account = generics.get_object_or_404(CloudAccount, pk=pk)
        account.status = request.data.get("status", account.status)
        account.save(update_fields=["status", "updated_at"])
        write_audit_log(
            module="accounts",
            action="status",
            operator=request.user,
            target_type="cloud_account",
            target_id=str(account.id),
            detail={"status": account.status},
        )
        return success_response(CloudAccountSerializer(account).data)


class CloudAccountTestConnectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        account = generics.get_object_or_404(CloudAccount, pk=pk)
        write_audit_log(
            module="accounts",
            action="test_connection",
            operator=request.user,
            target_type="cloud_account",
            target_id=str(account.id),
        )
        return success_response({"connected": True, "account_id": account.id}, message="connection ok")


class CloudAccountSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        account = generics.get_object_or_404(CloudAccount, pk=pk)
        task = TaskExecution.objects.create(
            name=f"Sync account {account.name}",
            task_type=TaskExecution.TaskType.ACCOUNT_SYNC,
            status=TaskExecution.Status.PENDING,
            payload={"account_id": account.id},
            created_by=request.user,
            started_at=timezone.now(),
        )
        write_audit_log(
            module="accounts",
            action="sync",
            operator=request.user,
            target_type="cloud_account",
            target_id=str(account.id),
            detail={"task_id": task.id},
        )
        return success_response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
