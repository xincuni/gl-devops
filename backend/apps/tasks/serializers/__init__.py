from rest_framework import serializers

from apps.tasks.models import TaskExecution


class TaskExecutionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = TaskExecution
        fields = "__all__"
