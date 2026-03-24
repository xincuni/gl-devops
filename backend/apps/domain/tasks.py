from celery import shared_task

from apps.accounts.models import CloudAccount
from apps.domain.services import seed_domain_sync


@shared_task(name="apps.domain.tasks.sync_domains")
def sync_domains():
    accounts = CloudAccount.objects.filter(
        provider__in=[CloudAccount.Provider.ALIYUN, CloudAccount.Provider.CLOUDFLARE]
    )
    task_ids = [seed_domain_sync(account=account, operator=None).id for account in accounts]
    return {"task_ids": task_ids, "count": len(task_ids)}
