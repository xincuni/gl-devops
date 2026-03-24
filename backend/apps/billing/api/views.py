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
    queryset = BillingLineItem.objects.select_related("account").all()
    serializer_class = BillingLineItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["provider", "account", "billing_month", "product", "resource_id", "normalized_env", "normalized_product"]
    search_fields = ["resource_id", "resource_name", "product"]
    ordering_fields = ["billing_date", "discounted_cost", "product", "provider"]


class BillingLineItemDetailView(generics.RetrieveAPIView):
    queryset = BillingLineItem.objects.select_related("account").all()
    serializer_class = BillingLineItemSerializer
    permission_classes = [permissions.IsAuthenticated]


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
