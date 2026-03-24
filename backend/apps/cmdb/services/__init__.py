from django.utils import timezone

from apps.accounts.models import CloudAccount
from apps.assets.models import CloudInstance
from apps.cmdb.models import CMDBAsset
from apps.domain.models import DNSRecord, DNSZone


def sync_cmdb_assets():
    now = timezone.now()

    for account in CloudAccount.objects.all():
        CMDBAsset.objects.update_or_create(
            asset_type=CMDBAsset.AssetType.CLOUD_ACCOUNT,
            source=account.provider,
            source_ref=str(account.id),
            defaults={
                "name": account.name,
                "status": account.status,
                "labels": {},
                "metadata": {"provider": account.provider},
                "last_synced_at": now,
            },
        )

    for instance in CloudInstance.objects.select_related("account").all():
        CMDBAsset.objects.update_or_create(
            asset_type=CMDBAsset.AssetType.CLOUD_INSTANCE,
            source=instance.provider,
            source_ref=instance.instance_id,
            defaults={
                "name": instance.instance_name,
                "status": instance.status,
                "labels": instance.tags_json,
                "metadata": {"region": instance.region, "account": instance.account.name},
                "last_synced_at": now,
            },
        )

    for zone in DNSZone.objects.select_related("account").all():
        CMDBAsset.objects.update_or_create(
            asset_type=CMDBAsset.AssetType.DNS_ZONE,
            source=zone.provider,
            source_ref=zone.zone_id,
            defaults={
                "name": zone.zone_name,
                "status": zone.status,
                "labels": {},
                "metadata": {"account": zone.account.name},
                "last_synced_at": now,
            },
        )

    for record in DNSRecord.objects.select_related("zone").all():
        CMDBAsset.objects.update_or_create(
            asset_type=CMDBAsset.AssetType.DNS_RECORD,
            source=record.zone.provider,
            source_ref=record.provider_record_id,
            defaults={
                "name": f"{record.name}.{record.zone.zone_name}",
                "status": record.status,
                "labels": {"type": record.type},
                "metadata": {"value": record.value, "zone": record.zone.zone_name},
                "last_synced_at": now,
            },
        )
