from django.db.models import Count
from rest_framework import permissions
from rest_framework.views import APIView

from apps.accounts.models import CloudAccount
from apps.assets.models import CloudInstance
from apps.billing.services import billing_overview
from apps.domain.models import DNSRecord, DNSZone
from apps.jumpserver.models import JumpServerSyncLog
from apps.tasks.models import TaskExecution
from common.responses import success_response


class PortalSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "accounts": {
                "total": CloudAccount.objects.count(),
                "active": CloudAccount.objects.filter(status=CloudAccount.Status.ACTIVE).count(),
            },
            "domains": {
                "zones": DNSZone.objects.count(),
                "records": DNSRecord.objects.count(),
            },
            "instances": {
                "total": CloudInstance.objects.count(),
                "running": CloudInstance.objects.filter(status=CloudInstance.Status.RUNNING).count(),
                "jumpserver_synced": CloudInstance.objects.filter(
                    jumpserver_sync_status=CloudInstance.JumpServerSyncStatus.SYNCED
                ).count(),
            },
            "billing": billing_overview(),
            "tasks": {
                "total": TaskExecution.objects.count(),
                "failed": TaskExecution.objects.filter(status=TaskExecution.Status.FAILED).count(),
                "pending": TaskExecution.objects.filter(status=TaskExecution.Status.PENDING).count(),
            },
            "jumpserver": {
                "sync_logs": JumpServerSyncLog.objects.count(),
                "success": JumpServerSyncLog.objects.filter(status=JumpServerSyncLog.Status.SUCCESS).count(),
            },
        }
        return success_response(data)


class PortalRecentTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rows = (
            TaskExecution.objects.select_related("created_by")
            .values("id", "name", "task_type", "status", "created_at", "created_by__username")
            .order_by("-created_at")[:8]
        )
        return success_response(list(rows))


class PortalAlertsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        alerts = []
        failed_tasks = TaskExecution.objects.filter(status=TaskExecution.Status.FAILED).count()
        pending_jumpserver = CloudInstance.objects.filter(
            jumpserver_sync_status=CloudInstance.JumpServerSyncStatus.PENDING
        ).count()
        dns_by_provider = list(DNSZone.objects.values("provider").annotate(total=Count("id")).order_by("provider"))

        if failed_tasks:
            alerts.append({"level": "high", "title": "存在失败任务", "value": failed_tasks})
        if pending_jumpserver:
            alerts.append({"level": "medium", "title": "待同步 JumpServer 主机", "value": pending_jumpserver})
        if not alerts:
            alerts.append({"level": "info", "title": "当前无阻塞告警", "value": 0})

        alerts.append({"level": "info", "title": "DNS Zone 分布", "value": dns_by_provider})
        return success_response(alerts)
