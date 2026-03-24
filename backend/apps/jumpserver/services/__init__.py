from django.utils import timezone

from apps.assets.models import CloudInstance
from apps.audit.services import write_audit_log
from apps.jumpserver.models import JumpServerSyncLog, JumpServerSyncRule
from apps.tasks.models import TaskExecution


def ensure_default_rule():
    rule, _ = JumpServerSyncRule.objects.get_or_create(
        name="默认 Linux 纳管规则",
        defaults={
            "provider": "",
            "region": "",
            "env": "",
            "node_path": "/Default/Cloud",
            "platform": "linux",
            "status": JumpServerSyncRule.Status.ACTIVE,
            "priority": 100,
            "extra_config": {"comment": "mock sync rule"},
        },
    )
    return rule


def match_rule(instance: CloudInstance):
    tags = instance.tags_json or {}
    queryset = JumpServerSyncRule.objects.filter(status=JumpServerSyncRule.Status.ACTIVE).order_by("priority", "id")
    for rule in queryset:
        if rule.provider and rule.provider != instance.provider:
            continue
        if rule.region and rule.region != instance.region:
            continue
        if rule.account_id and rule.account_id != instance.account_id:
            continue
        if rule.env and tags.get("env") != rule.env:
            continue
        return rule
    return ensure_default_rule()


def sync_instances_to_jumpserver(*, instances, operator=None):
    ensure_default_rule()
    synced = []
    now = timezone.now()

    for instance in instances:
        rule = match_rule(instance)
        asset_id = f"js-{instance.provider}-{instance.id}"
        instance.jumpserver_sync_status = CloudInstance.JumpServerSyncStatus.SYNCED
        instance.jumpserver_asset_id = asset_id
        instance.last_jumpserver_sync_at = now
        instance.save(update_fields=["jumpserver_sync_status", "jumpserver_asset_id", "last_jumpserver_sync_at", "updated_at"])

        JumpServerSyncLog.objects.create(
            rule=rule,
            instance=instance,
            jumpserver_asset_id=asset_id,
            status=JumpServerSyncLog.Status.SUCCESS,
            message="mock jumpserver sync completed",
            payload={"instance_id": instance.instance_id},
            result={"node_path": rule.node_path},
        )
        synced.append(instance.id)

    task = TaskExecution.objects.create(
        name=f"Sync {len(synced)} instances to JumpServer",
        task_type=TaskExecution.TaskType.JUMPSERVER_SYNC,
        status=TaskExecution.Status.SUCCESS,
        message="mock jumpserver sync completed",
        payload={"instance_ids": synced},
        result={"synced": len(synced)},
        created_by=operator,
        started_at=now,
        finished_at=now,
    )
    write_audit_log(
        module="jumpserver",
        action="sync_assets",
        operator=operator,
        target_type="cloud_instance",
        target_id=",".join(str(instance_id) for instance_id in synced),
        detail={"task_id": task.id, "count": len(synced)},
    )
    return task
