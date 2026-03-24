from celery import shared_task

from apps.billing.services import seed_billing_data


@shared_task(name="apps.billing.tasks.collect_billing")
def collect_billing():
    task = seed_billing_data(operator=None)
    return {"task_id": task.id, "task_type": "billing_collect"}
