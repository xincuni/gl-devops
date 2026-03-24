from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from apps.audit.models import AuditLog
from apps.audit.services import write_audit_log
from apps.domain.models import DNSRecord, DNSZone
from apps.domain.serializers import DNSRecordSerializer, DNSZoneSerializer
from apps.domain.services import seed_domain_sync
from common.responses import success_response


class DNSZoneListView(generics.ListAPIView):
    queryset = DNSZone.objects.select_related("account").all()
    serializer_class = DNSZoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["provider", "account", "status"]
    search_fields = ["zone_name"]


class DNSZoneDetailView(generics.RetrieveAPIView):
    queryset = DNSZone.objects.select_related("account").all()
    serializer_class = DNSZoneSerializer
    permission_classes = [permissions.IsAuthenticated]


class DNSZoneSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        zone = generics.get_object_or_404(DNSZone, pk=pk)
        task = seed_domain_sync(account=zone.account, operator=request.user)
        return success_response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class DNSRecordListView(generics.ListAPIView):
    queryset = DNSRecord.objects.select_related("zone", "zone__account").all()
    serializer_class = DNSRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["zone", "type", "status", "zone__provider"]
    search_fields = ["name", "value"]


class DNSRecordDetailView(generics.RetrieveAPIView):
    queryset = DNSRecord.objects.select_related("zone", "zone__account").all()
    serializer_class = DNSRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        record = self.get_object()
        response = super().retrieve(request, *args, **kwargs)
        audits = AuditLog.objects.filter(
            target_type="dns_zone",
            target_id=str(record.zone.id),
        )[:10]
        response.data["audits"] = [
            {
                "id": item.id,
                "module": item.module,
                "action": item.action,
                "operator": item.operator.username if item.operator else "",
                "detail": item.detail,
                "created_at": item.created_at,
            }
            for item in audits
        ]
        return response


class DNSRecordBatchStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, target_status):
        record_ids = request.data.get("record_ids", [])
        records = list(DNSRecord.objects.filter(id__in=record_ids))
        DNSRecord.objects.filter(id__in=record_ids).update(status=target_status)
        for record in records:
            write_audit_log(
                module="domain",
                action=f"record_status_{target_status}",
                operator=request.user,
                target_type="dns_record",
                target_id=str(record.id),
                detail={"zone_id": record.zone_id},
            )
        return success_response({"updated": len(records)})


class DNSRecordBatchTTLView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        record_ids = request.data.get("record_ids", [])
        ttl = int(request.data.get("ttl", 600))
        records = list(DNSRecord.objects.filter(id__in=record_ids))
        DNSRecord.objects.filter(id__in=record_ids).update(ttl=ttl)
        for record in records:
            write_audit_log(
                module="domain",
                action="record_update_ttl",
                operator=request.user,
                target_type="dns_record",
                target_id=str(record.id),
                detail={"zone_id": record.zone_id, "ttl": ttl},
            )
        return success_response({"updated": len(records), "ttl": ttl})
