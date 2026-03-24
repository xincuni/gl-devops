from celery import shared_task

from apps.assets.models import CloudInstance
from apps.jumpserver.services import sync_instances_to_jumpserver


@shared_task(name="apps.jumpserver.tasks.sync_to_jumpserver")
def sync_to_jumpserver():
    task = sync_instances_to_jumpserver(instances=list(CloudInstance.objects.all()[:20]), operator=None)
    return {"task_id": task.id, "task_type": "jumpserver_sync"}
