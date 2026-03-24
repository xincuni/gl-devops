import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

import AppLayout from "../layouts/AppLayout.vue";
import DomainsLayout from "../layouts/DomainsLayout.vue";
import LoginPage from "../pages/auth/LoginPage.vue";
import AccountsPage from "../pages/accounts/AccountsPage.vue";
import RecordDetailPage from "../pages/domains/RecordDetailPage.vue";
import ZonesPage from "../pages/domains/ZonesPage.vue";
import RecordsPage from "../pages/domains/RecordsPage.vue";
import TasksPage from "../pages/tasks/TasksPage.vue";

const routes = [
  { path: "/login", component: LoginPage, meta: { guestOnly: true } },
  {
    path: "/",
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      { path: "", redirect: "/accounts" },
      { path: "accounts", component: AccountsPage },
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
    return "/accounts";
  }

  return true;
});

export default router;
