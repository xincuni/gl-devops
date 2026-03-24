import json

from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Create default periodic task templates for billing, domain, asset, and jumpserver sync"

    def handle(self, *args, **options):
        hourly, _ = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="*",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone="Asia/Shanghai",
        )
        daily, _ = CrontabSchedule.objects.get_or_create(
            minute="30",
            hour="2",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone="Asia/Shanghai",
        )

        task_templates = [
            ("Billing Collect", "apps.billing.tasks.collect_billing", daily),
            ("Domain Sync", "apps.domain.tasks.sync_domains", hourly),
            ("Asset Sync", "apps.assets.tasks.sync_instances", hourly),
            ("JumpServer Sync", "apps.jumpserver.tasks.sync_to_jumpserver", hourly),
        ]

        for name, task, schedule in task_templates:
            PeriodicTask.objects.update_or_create(
                name=name,
                defaults={
                    "task": task,
                    "crontab": schedule,
                    "enabled": False,
                    "kwargs": json.dumps({}),
                    "description": f"Bootstrap template for {task}",
                },
            )

        self.stdout.write(self.style.SUCCESS("Periodic task templates created"))
