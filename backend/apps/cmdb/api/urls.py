from django.urls import path

from apps.cmdb.api.views import CMDBAssetDetailView, CMDBAssetListView, CMDBSyncView

urlpatterns = [
    path("assets", CMDBAssetListView.as_view(), name="cmdb_asset_list"),
    path("assets/<int:pk>", CMDBAssetDetailView.as_view(), name="cmdb_asset_detail"),
    path("sync", CMDBSyncView.as_view(), name="cmdb_sync"),
]
