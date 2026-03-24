import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

import AppLayout from "../layouts/AppLayout.vue";
import AssetsLayout from "../layouts/AssetsLayout.vue";
import BillingLayout from "../layouts/BillingLayout.vue";
import DomainsLayout from "../layouts/DomainsLayout.vue";
import LoginPage from "../pages/auth/LoginPage.vue";
import AccountsPage from "../pages/accounts/AccountsPage.vue";
import InstanceDetailPage from "../pages/assets/InstanceDetailPage.vue";
import InstancesPage from "../pages/assets/InstancesPage.vue";
import AnalysisPage from "../pages/billing/AnalysisPage.vue";
import OverviewPage from "../pages/billing/OverviewPage.vue";
import AssetDetailPage from "../pages/cmdb/AssetDetailPage.vue";
import AssetsPage from "../pages/cmdb/AssetsPage.vue";
import RecordDetailPage from "../pages/domains/RecordDetailPage.vue";
import ZonesPage from "../pages/domains/ZonesPage.vue";
import RecordsPage from "../pages/domains/RecordsPage.vue";
import RulesPage from "../pages/jumpserver/RulesPage.vue";
import SyncLogsPage from "../pages/jumpserver/SyncLogsPage.vue";
import PortalPage from "../pages/portal/PortalPage.vue";
import TasksPage from "../pages/tasks/TasksPage.vue";

const routes = [
  { path: "/login", component: LoginPage, meta: { guestOnly: true } },
  {
    path: "/",
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      { path: "", redirect: "/portal" },
      { path: "portal", component: PortalPage },
      { path: "accounts", component: AccountsPage },
      {
        path: "assets",
        component: AssetsLayout,
        children: [
          { path: "", redirect: "/assets/instances" },
          { path: "instances", component: InstancesPage },
          { path: "instances/:id", component: InstanceDetailPage },
        ],
      },
      {
        path: "billing",
        component: BillingLayout,
        children: [
          { path: "", redirect: "/billing/overview" },
          { path: "overview", component: OverviewPage },
          { path: "analysis", component: AnalysisPage },
        ],
      },
      {
        path: "cmdb",
        component: AssetsLayout,
        children: [
          { path: "", redirect: "/cmdb/assets" },
          { path: "assets", component: AssetsPage },
          { path: "assets/:id", component: AssetDetailPage },
        ],
      },
      {
        path: "jumpserver",
        component: AssetsLayout,
        children: [
          { path: "", redirect: "/jumpserver/rules" },
          { path: "rules", component: RulesPage },
          { path: "sync-logs", component: SyncLogsPage },
        ],
      },
      {
        path: "domains",
        component: DomainsLayout,
        children: [
          { path: "", redirect: "/domains/zones" },
          { path: "zones", component: ZonesPage },
          { path: "records", component: RecordsPage },
          { path: "records/:id", component: RecordDetailPage },
        ],
      },
      { path: "tasks", component: TasksPage },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const authStore = useAuthStore();
  const isAuthenticated = await authStore.ensureAuth();

  if (to.meta.requiresAuth && !isAuthenticated) {
    return "/login";
  }

  if (to.meta.guestOnly && isAuthenticated) {
    return "/portal";
  }

  return true;
});

export default router;
