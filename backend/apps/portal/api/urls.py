from django.urls import path

from apps.portal.api.views import PortalAlertsView, PortalRecentTasksView, PortalSummaryView

urlpatterns = [
    path("summary", PortalSummaryView.as_view(), name="portal_summary"),
    path("recent-tasks", PortalRecentTasksView.as_view(), name="portal_recent_tasks"),
    path("alerts", PortalAlertsView.as_view(), name="portal_alerts"),
]
