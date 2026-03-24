import csv

from django.http import HttpResponse
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from apps.billing.models import BillingLineItem
from apps.billing.serializers import BillingLineItemSerializer
from apps.billing.services import (
    analysis_by_account,
    analysis_by_dimension,
    analysis_by_resource,
    analysis_trend,
    billing_overview,
    seed_billing_data,
)
from apps.tasks.models import TaskExecution
from common.responses import success_response


def build_line_item_queryset(request):
    queryset = BillingLineItem.objects.select_related("account").all()
    filters = {
        "provider": request.query_params.get("provider"),
        "account_id": request.query_params.get("account"),
        "billing_month": request.query_params.get("billing_month"),
        "product": request.query_params.get("product"),
        "resource_id": request.query_params.get("resource_id"),
        "normalized_env": request.query_params.get("normalized_env"),
        "normalized_product": request.query_params.get("normalized_product"),
        "currency": request.query_params.get("currency"),
    }
    for field, value in filters.items():
        if value:
            queryset = queryset.filter(**{field: value})

    keyword = request.query_params.get("search")
    if keyword:
        queryset = queryset.filter(
            Q(resource_name__icontains=keyword)
            | Q(resource_id__icontains=keyword)
            | Q(product__icontains=keyword)
        )

    ordering = request.query_params.get("ordering")
    if ordering:
        queryset = queryset.order_by(ordering)
    return queryset


class BillingCollectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        task = seed_billing_data(operator=request.user)
        return success_response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class BillingRecollectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        BillingLineItem.objects.all().delete()
        task = seed_billing_data(operator=request.user)
        return success_response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class BillingCollectLogListView(generics.ListAPIView):
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        logs = TaskExecution.objects.filter(task_type=TaskExecution.TaskType.BILLING_COLLECT).values(
            "id",
            "name",
            "status",
            "message",
            "created_at",
            "started_at",
            "finished_at",
            "result",
        )
        return success_response(list(logs))


class BillingLineItemListView(generics.ListAPIView):
    serializer_class = BillingLineItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["provider", "account", "billing_month", "product", "resource_id", "normalized_env", "normalized_product", "currency"]
    search_fields = ["resource_id", "resource_name", "product"]
    ordering_fields = ["billing_date", "discounted_cost", "product", "provider"]

    def get_queryset(self):
        return build_line_item_queryset(self.request)


class BillingLineItemDetailView(generics.RetrieveAPIView):
    queryset = BillingLineItem.objects.select_related("account").all()
    serializer_class = BillingLineItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class BillingLineItemExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = build_line_item_queryset(request)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="billing-line-items.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "billing_month",
                "billing_date",
                "provider",
                "account",
                "currency",
                "product",
                "resource_id",
                "resource_name",
                "normalized_env",
                "normalized_product",
                "discounted_cost",
            ]
        )
        for item in queryset:
            writer.writerow(
                [
                    item.billing_month,
                    item.billing_date,
                    item.provider,
                    item.account.name,
                    item.currency,
                    item.product,
                    item.resource_id,
                    item.resource_name,
                    item.normalized_env,
                    item.normalized_product,
                    item.discounted_cost,
                ]
            )
        return response


class BillingOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(billing_overview())


class BillingAnalysisByEnvView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(analysis_by_dimension("env"))


class BillingAnalysisByProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(analysis_by_dimension("product"))


class BillingAnalysisByAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(analysis_by_account())


class BillingAnalysisByResourceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(analysis_by_resource())


class BillingAnalysisTrendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(analysis_trend())
