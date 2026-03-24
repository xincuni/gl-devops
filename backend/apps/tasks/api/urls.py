from django.urls import path

from apps.tasks.api.views import TaskExecutionDetailView, TaskExecutionListView

urlpatterns = [
    path("", TaskExecutionListView.as_view(), name="task_list"),
    path("<int:pk>", TaskExecutionDetailView.as_view(), name="task_detail"),
]
