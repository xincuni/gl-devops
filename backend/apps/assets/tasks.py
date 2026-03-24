from celery import shared_task

from apps.accounts.models import CloudAccount
from apps.assets.services import seed_instance_sync


@shared_task(name="apps.assets.tasks.sync_instances")
def sync_instances():
    accounts = CloudAccount.objects.filter(
        provider__in=[CloudAccount.Provider.ALIYUN, CloudAccount.Provider.AWS]
    )
    task_ids = [seed_instance_sync(account=account, operator=None).id for account in accounts]
    return {"task_ids": task_ids, "count": len(task_ids)}
