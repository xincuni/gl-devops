import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

import AppLayout from "../layouts/AppLayout.vue";
import LoginPage from "../pages/auth/LoginPage.vue";
import AccountsPage from "../pages/accounts/AccountsPage.vue";
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
