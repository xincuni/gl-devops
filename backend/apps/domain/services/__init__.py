from django.utils import timezone

from apps.accounts.models import CloudAccount
from apps.audit.services import write_audit_log
from apps.domain.models import DNSRecord, DNSZone
from apps.tasks.models import TaskExecution


def seed_domain_sync(*, account: CloudAccount, operator=None):
    zone, _ = DNSZone.objects.get_or_create(
        account=account,
        zone_id=f"{account.provider}-{account.id}-example-com",
        defaults={
            "provider": account.provider,
            "zone_name": f"{account.provider}-example.com",
            "status": DNSZone.Status.ACTIVE,
            "last_synced_at": timezone.now(),
        },
    )
    zone.last_synced_at = timezone.now()
    zone.save(update_fields=["last_synced_at", "updated_at"])

    records = [
        {
            "provider_record_id": f"{zone.id}-root-a",
            "name": "@",
            "type": "A",
            "value": "1.1.1.1",
            "ttl": 600,
        },
        {
            "provider_record_id": f"{zone.id}-www-cname",
            "name": "www",
            "type": "CNAME",
            "value": "@",
            "ttl": 600,
        },
    ]
    for item in records:
        DNSRecord.objects.update_or_create(
            zone=zone,
            provider_record_id=item["provider_record_id"],
            defaults={
                **item,
                "status": DNSRecord.Status.ACTIVE,
                "last_synced_at": timezone.now(),
            },
        )

    task = TaskExecution.objects.create(
        name=f"Sync DNS zone {zone.zone_name}",
        task_type=TaskExecution.TaskType.DNS_SYNC,
        status=TaskExecution.Status.SUCCESS,
        message="mock dns sync completed",
        payload={"account_id": account.id, "zone_id": zone.id},
        result={"records": 2},
        created_by=operator,
        started_at=timezone.now(),
        finished_at=timezone.now(),
    )
    write_audit_log(
        module="domain",
        action="sync_zone",
        operator=operator,
        target_type="dns_zone",
        target_id=str(zone.id),
        detail={"task_id": task.id, "zone_name": zone.zone_name},
    )
    return task
