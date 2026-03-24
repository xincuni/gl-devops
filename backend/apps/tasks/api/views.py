from rest_framework import generics, permissions

from apps.tasks.models import TaskExecution
from apps.tasks.serializers import TaskExecutionSerializer


class TaskExecutionListView(generics.ListAPIView):
    queryset = TaskExecution.objects.select_related("created_by").all()
    serializer_class = TaskExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["task_type", "status", "created_by"]
    search_fields = ["name"]


class TaskExecutionDetailView(generics.RetrieveAPIView):
    queryset = TaskExecution.objects.select_related("created_by").all()
    serializer_class = TaskExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
