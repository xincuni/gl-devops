from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.authentication.api.urls")),
    path("api/v1/accounts/", include("apps.accounts.api.urls")),
    path("api/v1/tasks/", include("apps.tasks.api.urls")),
    path("api/v1/audit/", include("apps.audit.api.urls")),
]
