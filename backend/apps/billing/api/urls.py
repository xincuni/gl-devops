from django.urls import path

from apps.billing.api.views import (
    BillingAnalysisByAccountView,
    BillingAnalysisByEnvView,
    BillingAnalysisByProductView,
    BillingAnalysisByResourceView,
    BillingAnalysisTrendView,
    BillingCollectLogListView,
    BillingCollectView,
    BillingLineItemDetailView,
    BillingLineItemExportView,
    BillingLineItemListView,
    BillingOverviewView,
    BillingRecollectView,
)

urlpatterns = [
    path("collect", BillingCollectView.as_view(), name="billing_collect"),
    path("recollect", BillingRecollectView.as_view(), name="billing_recollect"),
    path("collect-logs", BillingCollectLogListView.as_view(), name="billing_collect_logs"),
    path("line-items/export", BillingLineItemExportView.as_view(), name="billing_line_items_export"),
    path("line-items", BillingLineItemListView.as_view(), name="billing_line_items"),
    path("line-items/<int:pk>", BillingLineItemDetailView.as_view(), name="billing_line_item_detail"),
    path("overview", BillingOverviewView.as_view(), name="billing_overview"),
    path("analysis/by-env", BillingAnalysisByEnvView.as_view(), name="billing_analysis_env"),
    path("analysis/by-product", BillingAnalysisByProductView.as_view(), name="billing_analysis_product"),
    path("analysis/by-account", BillingAnalysisByAccountView.as_view(), name="billing_analysis_account"),
    path("analysis/by-resource", BillingAnalysisByResourceView.as_view(), name="billing_analysis_resource"),
    path("analysis/trend", BillingAnalysisTrendView.as_view(), name="billing_analysis_trend"),
]
