from django.utils import timezone

from apps.accounts.models import CloudAccount
from apps.assets.models import CloudInstance
from apps.audit.services import write_audit_log
from apps.tasks.models import TaskExecution


def seed_instance_sync(*, account: CloudAccount, operator=None):
    samples = [
        {
            "instance_id": f"{account.provider}-{account.id}-web-01",
            "instance_name": f"{account.provider.upper()} Web 01",
            "hostname": "web-01",
            "private_ip": "10.0.0.11",
            "public_ip": "8.8.8.11",
            "region": "cn-hangzhou" if account.provider == "aliyun" else "ap-southeast-1",
            "os_type": "linux",
            "status": CloudInstance.Status.RUNNING,
            "vpc_id": "vpc-demo-01",
            "subnet_id": "subnet-demo-01",
            "tags_json": {"env": "prod", "service": "web"},
        },
        {
            "instance_id": f"{account.provider}-{account.id}-job-01",
            "instance_name": f"{account.provider.upper()} Job 01",
            "hostname": "job-01",
            "private_ip": "10.0.0.21",
            "public_ip": "",
            "region": "cn-hangzhou" if account.provider == "aliyun" else "ap-southeast-1",
            "os_type": "linux",
            "status": CloudInstance.Status.STOPPED,
            "vpc_id": "vpc-demo-01",
            "subnet_id": "subnet-demo-02",
            "tags_json": {"env": "staging", "service": "job"},
        },
    ]
    for item in samples:
        CloudInstance.objects.update_or_create(
            account=account,
            instance_id=item["instance_id"],
            defaults={
                **item,
                "provider": account.provider,
                "sync_status": "synced",
                "last_synced_at": timezone.now(),
            },
        )

    task = TaskExecution.objects.create(
        name=f"Sync instances for {account.name}",
        task_type=TaskExecution.TaskType.INSTANCE_SYNC,
        status=TaskExecution.Status.SUCCESS,
        message="mock instance sync completed",
        payload={"account_id": account.id},
        result={"instances": len(samples)},
        created_by=operator,
        started_at=timezone.now(),
        finished_at=timezone.now(),
    )
    write_audit_log(
        module="assets",
        action="sync_instances",
        operator=operator,
        target_type="cloud_account",
        target_id=str(account.id),
        detail={"task_id": task.id},
    )
    return task
