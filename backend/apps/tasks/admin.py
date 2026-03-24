from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.tasks.models import TaskExecution


@admin.register(TaskExecution)
class TaskExecutionAdmin(ModelAdmin):
    list_display = ("id", "name", "task_type", "status", "created_by", "created_at")
    list_filter = ("task_type", "status")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at", "started_at", "finished_at")

# Register your models here.
